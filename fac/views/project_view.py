# -*- coding: utf-8 -*-
import quopri
from datetime import datetime
from threading import Thread

from dateutil.relativedelta import relativedelta

from django.core.exceptions import PermissionDenied
from django.db import connection
from django.db.models import Prefetch
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _

from accounts.models import Group

from fac.models import (
    Action,
    Budget,
    CategoryModel,
    Contact,
    Folder,
    ObjectiveAction,
    ObjectiveStatus,
    Organization,
    Period,
    Project,
    Status,
    Valorization,
)
from fac.serializers import (
    ExportActionsSerializer,
    ExportStatisticsSerializer,
    ProjectSerializer,
    ProjectStatisticsSerializer,
)

from helpers.views import ExpertRequiredApiView, ModelReadOnlyView

from .xlsx_fap_export import create_xlsx


def get_query_params_groups(request):
    """
    :request: the django request object
    :return: the Groups asked by the frontend and present in the GET queryparams,
             as a list of Group instances
    """
    query_params_groups = []
    if "groups" in request.GET:
        for group_pk in request.GET.get("groups", "").split(","):
            try:
                query_params_groups.append(int(group_pk))
            except ValueError:
                pass
    else:
        query_params_groups = {
            group.pk for group in request.user.group.laureate_groups.all()
        }

    groups_filter = []
    laureate_groups = {group.pk for group in request.user.group.laureate_groups.all()}
    laureate_groups.add(request.user.group.pk)
    for group_pk in query_params_groups:
        group = get_object_or_404(Group, pk=group_pk)
        if group.pk not in laureate_groups:
            raise PermissionDenied(_("Vous n'avez pas accès à ce groupe"))
        groups_filter.append(group)

    if not groups_filter:
        # if no group were provided, it's because the group has only access to his
        # group (not a pilot group).
        # so he doesn't have any choice in the frontend and we choose the filter
        # for him here, in the backend
        groups_filter.append(request.user.group)

    return groups_filter


class ProjectView(ModelReadOnlyView, ExpertRequiredApiView):
    """
    Project View
    """

    model = Project
    serializer = ProjectSerializer
    perm_module = "fac/project"
    updated_at_attribute_name = "updated_at"

    def get_serializer(self, request, call):
        if call == "GET":
            return ProjectStatisticsSerializer
        return self.serializer

    def filter(self, request, queryset):  # NOQA: A003
        """
        returns the project queryset, filtered for the groups asked by the user

        You can provide a GET parameter "groups" which is list of group PK joined on ','
        to filter out the projects having all these groups
        """

        groups_filter = get_query_params_groups(request)

        # filter the sub-objects to only include
        # the objects the user is authorized to see
        budgets_queryset = Budget.objects.filter(group__in=groups_filter).accessible_by(
            request.user
        )
        objectives_status_queryset = ObjectiveStatus.objects.filter(
            group__in=groups_filter
        ).accessible_by(request.user)
        objectives_action_queryset = ObjectiveAction.objects.filter(
            group__in=groups_filter
        ).accessible_by(request.user)

        queryset = queryset.prefetch_related(
            Prefetch(
                "folder_models__statuses__objectives",
                queryset=objectives_status_queryset,
                to_attr="user_status_objectives",
            )
        )
        queryset = queryset.prefetch_related(
            Prefetch(
                "folder_models__categories__action_models__objectives",
                queryset=objectives_action_queryset,
                to_attr="user_action_objectives",
            )
        )
        return (
            queryset.prefetch_related(
                Prefetch(
                    "project_budgets", queryset=budgets_queryset, to_attr="user_budgets"
                )
            )
            .accessible_by(request.user)
            .distinct()
        )

    def get_object(self, pk, request):
        project = super().get_object(pk, request)

        project.groups_filter = get_query_params_groups(request)
        self._populate_project(project.groups_filter, project, request)

        return project

    def _populate_project(self, groups_filter, project, request):
        (
            project.date_start,
            project.date_end,
            project.period,
        ) = self._parse_date_query_params(request.GET)
        project.actions = list(
            Action.objects.filter(
                folder__model__project=project,
                done=True,
                folder__owning_group__in=groups_filter,
            ).prefetch_related(
                "model__category_model",
                "valorization__period",
                "valorization__type_valorization",
                "folder__owning_group",
                "folder__model",
                "folder__linked_object",
                "files",
                "contact",
            )
        )
        project.all_folders = list(
            Folder.objects.filter(owning_group__in=groups_filter).prefetch_related(
                "owning_group", "actions__model", "model__statuses__action_models"
            )
        )
        for folder in project.all_folders:
            folder.cached_status = folder.get_status(project.date_end)
        project.all_statuses = list(
            Status.objects.all().prefetch_related("folder_model")
        )
        project.status_objectives = list(
            ObjectiveStatus.objects.filter(group__in=groups_filter).prefetch_related(
                "group", "period", "status__folder_model"
            )
        )
        project.action_objectives = list(
            ObjectiveAction.objects.filter(group__in=groups_filter).prefetch_related(
                "group", "period", "model_action__category_model__folder_model"
            )
        )
        project.all_categories = list(
            CategoryModel.objects.all().prefetch_related(
                "action_models__valorizations", "folder_model"
            )
        )
        project.all_valorizations = list(
            Valorization.objects.filter(
                type_valorization__groups__in=groups_filter
            ).prefetch_related("period", "type_valorization__groups")
        )
        project.all_budgets = list(
            Budget.objects.filter(project=project).prefetch_related("group", "period")
        )
        self._variable_populate_project(groups_filter, project)

    @staticmethod
    def _groups_intersect(groups, groups_filter):
        first_set = {group.pk for group in groups}
        second_set = {group.pk for group in groups_filter}
        return bool(first_set.intersection(second_set))

    def _variable_populate_project(self, groups_filter, project):  # NOQA: CFQ001
        project.budget_summary = self._extract_budget_stats(groups_filter, project)
        project.folder_models_statistics = {}

        # retrieve all done actions for this `folder_model` and `groups_filter`
        actions = [
            action
            for action in project.actions
            if action.folder.owning_group in groups_filter
        ]

        valorizations_per_group = [
            valorization
            for valorization in project.all_valorizations
            if self._groups_intersect(
                valorization.type_valorization.groups.all(), groups_filter
            )
        ]

        if project.period:
            # if the user specified a period, we need to further filter out
            # the actions done in the timespan of the period
            actions = [
                action
                for action in actions
                if project.date_end >= action.date >= project.date_start
            ]
            status_objectives_per_groups = [
                objective
                for objective in project.status_objectives
                if objective.period.pk == project.period.pk
                and objective.group in groups_filter
            ]
            action_objectives_per_groups = [
                objective
                for objective in project.action_objectives
                if objective.period.pk == project.period.pk
                and objective.group in groups_filter
            ]
            valorizations_per_group = [
                valorization
                for valorization in valorizations_per_group
                if valorization.period.pk == project.period.pk
            ]

        folders_per_groups = [
            folder
            for folder in project.all_folders
            if folder.owning_group in groups_filter
        ]

        for folder_model in project.folder_models.all():
            folder_model_actions = [
                action
                for action in actions
                if action.folder.model.pk == folder_model.pk
            ]
            folders = [
                folder
                for folder in folders_per_groups
                if folder.model.pk == folder_model.pk
            ]
            folder_model_statuses = [
                status
                for status in project.all_statuses
                if status.folder_model.pk == folder_model.pk
            ]
            folder_model_statuses.sort(key=lambda status: status.order, reverse=True)

            # if the user specified a period, we can also show the objectives (if any)
            # for this given period
            if project.period:
                status_objectives = [
                    objective
                    for objective in status_objectives_per_groups
                    if objective.status.folder_model.pk == folder_model.pk
                ]
                action_objectives = [
                    objective
                    for objective in action_objectives_per_groups
                    if objective.model_action.category_model.folder_model.pk
                    == folder_model.pk
                ]
            else:
                status_objectives = []
                action_objectives = []

            categories = [
                category
                for category in project.all_categories
                if category.folder_model.pk == folder_model.pk
            ]
            for category in categories:
                for model in category.action_models.all():
                    model.stats_valorizations = [
                        valorization
                        for valorization in valorizations_per_group
                        if valorization in model.valorizations.all()
                    ]

            project.folder_models_statistics[
                folder_model.pk
            ] = self._retrieve_folder_models_infos(
                groups_filter,
                folder_model,
                folder_model_actions,
                folders,
                folder_model_statuses,
                action_objectives,
                status_objectives,
                categories,
            )

    @staticmethod
    def _parse_date_query_params(query_params):
        """
        :query_params: the GET query params representing
                             the dates sent by the frontend
        :return: date_start (python date object),
                 date_end (python date object),
                 period (Period model)
        """
        if not query_params.get("period"):
            return None, None, None

        period = get_object_or_404(Period, pk=query_params["period"])

        if query_params.get("date_start"):
            date_start_asked = datetime.strptime(
                query_params["date_start"], "%Y-%m-%d"
            ).date()
        else:
            date_start_asked = period.date_start

        if query_params.get("date_end"):
            date_end_asked = datetime.strptime(
                query_params["date_end"], "%Y-%m-%d"
            ).date()
        else:
            date_end_asked = period.date_end

        date_start = max(period.date_start, date_start_asked)
        date_end = min(period.date_end, date_end_asked)

        return date_start, date_end, period

    @staticmethod  # NOQA: CFQ002
    def _retrieve_folder_models_infos(
        groups_filter,
        folder_model,
        actions,
        folders,
        folder_model_statuses,
        action_objectives,
        status_objectives,
        categories,
    ):
        # for each status of this `folder_model`, count the number of `Folder`s
        # having this status
        nb_using_the_folder_model = len(folders)
        nb_folders_by_statuses = {}
        for folder in folders:
            nb_folders_by_statuses[folder.cached_status.pk] = (
                nb_folders_by_statuses.get(folder.cached_status.pk, 0) + 1
            )
        statuses = {}
        statuses_sum = 0
        for status in folder_model_statuses:
            nb_statuses = nb_folders_by_statuses.get(status.pk, 0)
            # we also keep count of the total accumulated number of statuses.
            # For example having a status "Partner" (order=5) obviously means having
            # lower statuses like "Contacted" (order=2).
            # That's why we need to start from the "biggest" status
            # (see `.sort(key=lambda status: status.order, reverse=True)`)
            statuses_sum += nb_statuses

            try:
                percentage_using_the_folder = (
                    nb_statuses * 100 / nb_using_the_folder_model
                )
            except ZeroDivisionError:
                percentage_using_the_folder = 0

            statuses[status.pk] = {
                "pk": status.pk,
                "name": status.name,
                "order": status.order,
                "nb_total": statuses_sum,
                "nb_exact": nb_statuses,
                "percentage_using_the_folder": percentage_using_the_folder,
            }

        for status_objective in status_objectives:
            statuses[status_objective.status.pk]["objective"] = (
                statuses[status_objective.status.pk].get("objective", 0)
                + status_objective.nb_statuses
            )

        action_objectives_dict = {}
        for action_objective in action_objectives:
            # -action_objectives_dict = {
            # -  category_pk_1: {
            # -    action_model_pk_1: objective.nb_actions,
            # -    ...
            # -  },
            # -  ...
            # -}
            action_model = action_objective.model_action
            category_pk = action_model.category_model.pk
            existing_objectives = action_objectives_dict.get(category_pk, {})
            existing_objectives[action_model.pk] = (
                existing_objectives.get(action_model.pk, 0)
                + action_objective.nb_actions
            )
            action_objectives_dict[category_pk] = existing_objectives

        return {
            "has_status_objectives": len(status_objectives) > 0,
            "has_action_objectives": len(action_objectives_dict) > 0,
            "action_objectives": action_objectives_dict,
            "actions_queryset": actions,
            "categories": categories,
            "statuses": sorted(statuses.values(), key=lambda status: status["order"]),
            "name": folder_model.name,
            "groups": groups_filter,
        }

    @staticmethod
    def _extract_budget_stats(groups_filter, project):
        if not project.period:
            return None

        budgets = [
            budget
            for budget in project.all_budgets
            if budget.group in groups_filter and budget.period.pk == project.period.pk
        ]

        last_action = [
            action
            for action in project.actions
            if action.folder.owning_group in groups_filter
            and project.period.date_start <= action.date <= project.date_end
        ]
        last_action.sort(key=lambda action: action.date, reverse=True)
        if last_action:
            last_action = last_action[0]

        if not budgets:
            return None

        last_action_date = project.date_start
        if last_action:
            last_action_date = last_action.date

        # Each step will contains :
        # - date: the end date of the time lapse
        # - expenses: The total expenses of the budget at the step date
        graph_data = []
        point_date = project.date_start
        date_increment = relativedelta(months=1)

        # Prepare all the periods
        while point_date < last_action_date:
            graph_data.append({"date": point_date, "cumulated_expenses": 0.0})
            point_date += date_increment

        # the last point should be exactly on the last action
        graph_data.append({"date": last_action_date, "cumulated_expenses": 0.0})
        budget_summaries = []
        for budget in budgets:
            budget_summaries.append(
                budget.budget_summary(
                    graph_start=project.date_start,
                    graph_end=last_action_date,
                    graph_data=graph_data,
                    all_actions=project.actions,
                )
            )

        total_budget_summary = {
            "graph_data": graph_data,
            "total_envelope": sum(
                budget_summary["total_envelope"] for budget_summary in budget_summaries
            ),
            "total_expenses": sum(
                budget_summary["total_expenses"] for budget_summary in budget_summaries
            ),
            "expenses_in_selected_time_lapse": sum(
                budget_summary["expenses_in_selected_time_lapse"]
                for budget_summary in budget_summaries
            ),
            "period_start": project.date_start,
            "period_end": project.date_end,
        }
        try:
            total_budget_summary["pourcent_expenses"] = (
                total_budget_summary["total_expenses"]
                / total_budget_summary["total_envelope"]
            ) * 100
        except ZeroDivisionError:
            total_budget_summary["pourcent_expenses"] = 0

        return total_budget_summary

    def detail(self, request, *args, **kwargs):
        if request.GET.get("export") == "1":
            if request.GET.get("send_report_by_mail") == "true":
                return self.export_by_mail(request, *args, **kwargs)
            else:
                return self.export(request, *args, **kwargs)

        return super().detail(request, *args, **kwargs)

    def prepare_report(self, request, *args, **kwargs):
        project = self.get_object(kwargs["pk"], request)

        perm = self.get_perm_module(request, "GET")
        if perm and not request.user.has_perm(f"{perm}.view", project):
            raise PermissionDenied

        export_type = request.GET.get("export_type")
        if export_type == "actions":
            project.organizations = {
                organization.pk: {
                    "name": organization.name,
                    "email": organization.email,
                    "type": organization.type_of_organization,
                    "tags": [tag.name for tag in organization.tags.all()],
                    "town": organization.town,
                    "zipcode": organization.zipcode,
                    "address": organization.address,
                    "nb_contacts": len(organization.memberoforganization_set.all()),
                    "members": {
                        member.contact.pk: member.title_in_organization
                        for member in organization.memberoforganization_set.all()
                    },
                    "referent": ", ".join(
                        f"{referent.last_name} {referent.first_name}"
                        for referent in organization.referents.all()
                    ),
                }
                for organization in Organization.objects.filter(
                    owning_group__in=project.groups_filter
                ).prefetch_related("tags", "memberoforganization_set", "referents")
            }

            project.contacts = {
                contact.pk: {
                    "name": f"{contact.last_name} {contact.first_name}",
                    "email": contact.email,
                    "type": "Contact",
                    "tags": [tag.name for tag in contact.tags.all()],
                    "town": contact.town,
                    "zipcode": contact.zipcode,
                    "address": contact.address,
                    "referent": ", ".join(
                        f"{referent.last_name} {referent.first_name}"
                        for referent in contact.referents.all()
                    ),
                }
                for contact in Contact.objects.filter(
                    owning_group__in=project.groups_filter
                ).prefetch_related("tags", "referents")
            }
            serializer = ExportActionsSerializer
        else:
            serializer = ExportStatisticsSerializer

        project_statistics = serializer(project).data

        project_statistics_laureates = []
        selected_groups = project.groups_filter

        if len(project.groups_filter) > 1:
            for group in selected_groups:
                # TODO: re-write the code so that we don't need to call this
                self._variable_populate_project([group], project)
                project_statistics_laureates.append((group, serializer(project).data))
        filename, file_bytes = create_xlsx(
            [str(group) for group in selected_groups],
            project_statistics,
            project_statistics_laureates,
            export_actions=export_type == "actions",
            export_statistics=export_type == "statistics",
        )

        return {
            "filename": filename,
            "file_bytes": file_bytes,
        }

    def export_by_mail(self, request, *args, **kwargs):
        project = self.get_object(kwargs["pk"], request)

        perm = self.get_perm_module(request, "GET")
        if perm and not request.user.has_perm(f"{perm}.view", project):
            raise PermissionDenied

        kwargs["mixeur_request"] = request
        t = Thread(target=self.threaded_export_by_mail, args=args, kwargs=kwargs)
        t.daemon = True
        t.start()
        return JsonResponse(
            {
                "return": "OK",
            }
        )

    def threaded_export_by_mail(self, *args, **kwargs):
        # Not the best solution… but no idea to do better
        # WARN: if an user click many times, it could increase cpuload too much
        # https://stackoverflow.com/questions/18420699/multithreading-for-python-django
        request = kwargs["mixeur_request"]
        del kwargs["mixeur_request"]
        generated_file = self.prepare_report(request, *args, **kwargs)

        # send to user by mail
        user = request.user
        user.send_email(
            subject="Rapport de statistiques Mixeur",
            html_message="<p>Bonjour {{user.full_name}}</p><p>Vous trouverez ci-joint le rapport que vous avez demandé.</p>",  # NOQA: E501
            context={},
            attachments=[
                {
                    "filename": generated_file["filename"],
                    "content": quopri.encodestring(generated_file["file_bytes"]).decode(
                        "utf-8"
                    ),
                    "mimetype": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                }
            ],
        )

        connection.close()

    def export(self, request, *args, **kwargs):
        project = self.get_object(kwargs["pk"], request)

        perm = self.get_perm_module(request, "GET")
        if perm and not request.user.has_perm(f"{perm}.view", project):
            raise PermissionDenied

        generated_file = self.prepare_report(request, *args, **kwargs)

        response = HttpResponse(
            content=generated_file["file_bytes"],
            content_type="application/"
            "vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )

        response[
            "Content-Disposition"
        ] = f"attachment; filename={generated_file['filename']}"

        return response

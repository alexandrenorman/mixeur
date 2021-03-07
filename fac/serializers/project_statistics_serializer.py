from decimal import Decimal

import serpy

from .action_export_serializer import ActionExportSerializer
from .action_serializer import ActionDocumentSerializer

NO_VALORIZATION_KEY = "Non valorisé"


class CategoryStatisticsSerializer(serpy.Serializer):
    name = serpy.MethodField()
    total_actions = serpy.MethodField()
    actions = serpy.MethodField()
    objective = serpy.MethodField()
    progression = serpy.MethodField()
    total_expenses = serpy.MethodField()

    def get_total_expenses(self, category):
        return sum(
            action.cost
            for actions_per_model in category["actions"].values()
            for action in actions_per_model
        )

    def get_name(self, category):
        return category["name"]

    def get_actions(self, category):  # NOQA: CFQ001
        actions = []

        for action_model in category["action_models"]:
            actions_of_model = category["actions"][action_model.pk]

            total = len(actions_of_model)
            objective = category["objectives"].get(action_model.pk, 0)
            try:
                progression = 100 * total / objective
            except ZeroDivisionError:
                progression = "-"

            (
                actions_per_valorization_types,
                actions_per_valorization_types_coefficient,
                is_act_per_valorization_types,
                unit_valorization_per_valorization_types,
            ) = self._init_from_valorizations(action_model, category)

            for action in actions_of_model:
                try:
                    type_valorization = action.valorization.type_valorization.name
                except AttributeError:
                    actions_per_valorization_types[
                        NO_VALORIZATION_KEY
                    ] = actions_per_valorization_types.get(NO_VALORIZATION_KEY, []) + [
                        action
                    ]
                    continue

                if (
                    action_model.coefficient_enabled
                    and action.owning_group.coefficient < Decimal("1")
                ):
                    type_valorization = f"{action.owning_group}"
                    actions_per_valorization_types_coefficient[
                        type_valorization
                    ].append(action)
                else:
                    actions_per_valorization_types[type_valorization].append(action)

            groups = category["groups"]
            if (
                len(groups)
                == len(actions_per_valorization_types)
                == len(actions_per_valorization_types_coefficient)
                == 1
                and len(list(actions_per_valorization_types.values())[0]) == 0
                and list(actions_per_valorization_types_coefficient.keys())[0]
                == f"{groups[0]}"
            ):
                # special case: we are viewing the stats of a single group.
                #   This group has a coefficient for this action_model, then we
                #   shouldn't see the Valorization of the action_model, only the one
                #   ponderated for this specific group
                actions_per_valorization_types = {}

            # add them after, so that the ones with a coefficient are displayed after
            # the "normal" ones
            actions_per_valorization_types.update(
                actions_per_valorization_types_coefficient
            )

            type_valorizations = list(actions_per_valorization_types.keys())
            quantities = [
                sum(action.quantity for action in actions)
                for actions in actions_per_valorization_types.values()
            ]
            unit_valorizations = [
                unit_valorization_per_valorization_types[type_valorization]
                for type_valorization in type_valorizations
            ]
            is_act = [
                is_act_per_valorization_types[type_valorization]
                for type_valorization in type_valorizations
            ]
            total_valorisations = [
                sum(action.cost for action in actions)
                for actions in actions_per_valorization_types.values()
            ]

            type_valorizations = [
                type_valorization if type_valorization != NO_VALORIZATION_KEY else ""
                for type_valorization in type_valorizations
            ]
            if not actions_per_valorization_types:
                # If no valorization is present, we fill an empty line
                # so that the tables arent empty
                type_valorizations = [""]
                quantities = unit_valorizations = total_valorisations = [0]

            actions_with_files = self._get_actions_with_mandatory_files(
                action_model, actions_of_model
            )

            actions.append(
                {
                    "name": action_model.name,
                    "model": action_model.pk,
                    "total": total,
                    "quantity": quantities,
                    "objective": objective,
                    "progression": progression,
                    "unit_valorisation": unit_valorizations,
                    "type_valorizations": type_valorizations,
                    "total_valorisation": total_valorisations,
                    "is_act": is_act,
                    "actions_with_files": actions_with_files,
                }
            )

        return actions

    @staticmethod
    def _get_actions_with_mandatory_files(action_model, actions_of_model):
        actions_with_files = {}
        if action_model.file_required:
            for action in actions_of_model:
                folder_owner = f"{action.folder.owning_group}"
                actions_with_files[folder_owner] = actions_with_files.get(
                    folder_owner, []
                ) + [ActionDocumentSerializer(action).data]
        return actions_with_files

    @staticmethod
    def _init_from_valorizations(action_model, category):
        actions_per_valorization_types = {}
        actions_per_valorization_types_coefficient = {}
        unit_valorization_per_valorization_types = {NO_VALORIZATION_KEY: 0}
        is_act_per_valorization_types = {NO_VALORIZATION_KEY: True}
        for valorization in category["valorizations"][action_model.pk]:
            is_act_per_valorization_types[
                valorization.type_valorization.name
            ] = valorization.act
            unit_valorization = float(valorization.amount)
            unit_valorization_per_valorization_types[
                valorization.type_valorization.name
            ] = unit_valorization
            actions_per_valorization_types[valorization.type_valorization.name] = []

            for owning_group in category["groups"]:
                if (
                    action_model.coefficient_enabled
                    and owning_group.coefficient < Decimal("1")
                ):
                    name = f"{owning_group}"
                    is_act_per_valorization_types[name] = valorization.act
                    unit_valorization_per_valorization_types[
                        name
                    ] = unit_valorization * float(owning_group.coefficient)
                    actions_per_valorization_types_coefficient[name] = []
        return (
            actions_per_valorization_types,
            actions_per_valorization_types_coefficient,
            is_act_per_valorization_types,
            unit_valorization_per_valorization_types,
        )

    def get_total_actions(self, category):
        return sum(
            len(actions_per_model) for actions_per_model in category["actions"].values()
        )

    def get_objective(self, category):
        return sum(category["objectives"].values())

    def get_progression(self, category):
        try:
            return (100 * self.get_total_actions(category)) / self.get_objective(
                category
            )
        except ZeroDivisionError:
            return "-"


class StatusStatisticsSerializer(serpy.Serializer):
    pk = serpy.MethodField()
    name = serpy.MethodField()
    nb_status = serpy.MethodField()
    percentage_nb_organizations = serpy.MethodField()
    nb_cumulated = serpy.MethodField()
    objective = serpy.MethodField()
    progression = serpy.MethodField()

    def get_pk(self, status):
        return status["pk"]

    def get_name(self, status):
        return status["name"]

    def get_nb_status(self, status):
        return status["nb_exact"]

    def get_percentage_nb_organizations(self, status):
        return status["percentage_using_the_folder"]

    def get_nb_cumulated(self, status):
        return status["nb_total"]

    def get_objective(self, status):
        return status.get("objective")

    def get_progression(self, status):
        if status.get("objective", 0) > 0:
            return status["nb_total"] * 100 / status["objective"]
        return None


class FolderModelStatisticsSerializer(serpy.Serializer):
    categories = serpy.MethodField()
    statuses = serpy.MethodField()
    has_status_objectives = serpy.MethodField()
    has_action_objectives = serpy.MethodField()
    name = serpy.MethodField()
    total_expenses = serpy.MethodField()

    def get_total_expenses(self, folder_model):
        return sum(action.cost for action in folder_model["actions_queryset"])

    def get_name(self, folder_model):
        return folder_model["name"]

    def get_categories(self, folder_model):
        categories = {}
        groups = folder_model["groups"]

        for category in folder_model["categories"]:
            categories[category.pk] = {
                "actions": {
                    action_model.pk: [] for action_model in category.action_models.all()
                },
                "valorizations": {
                    action_model.pk: list(action_model.stats_valorizations)
                    for action_model in category.action_models.all()
                },
                "action_models": sorted(
                    category.action_models.all(),
                    key=lambda action_model: action_model.order,
                ),
                "name": category.name,
                "order": category.order,
                "objectives": folder_model["action_objectives"].get(category.pk, {}),
                "groups": groups,
            }

        for action in folder_model["actions_queryset"]:
            category_pk = action.model.category_model.pk
            categories[category_pk]["actions"][action.model.pk].append(action)

        # sort categories
        categories = sorted(categories.values(), key=lambda category: category["order"])

        return CategoryStatisticsSerializer(categories, many=True).data

    def get_statuses(self, folder_model):
        return StatusStatisticsSerializer(folder_model["statuses"], many=True).data

    def get_has_action_objectives(self, folder_model):
        return folder_model["has_action_objectives"]

    def get_has_status_objectives(self, folder_model):
        return folder_model["has_status_objectives"]


class ProjectStatisticsSerializer(serpy.Serializer):
    folder_models = serpy.MethodField()
    budget_tracking = serpy.MethodField()
    custom_display_fields = serpy.MethodField()
    name = serpy.MethodField()
    date_start = serpy.MethodField()
    date_end = serpy.MethodField()

    def get_name(self, project):
        return project.name

    def get_date_start(self, project):
        if project.date_start:
            return project.date_start.strftime("%d/%m/%Y")

    def get_date_end(self, project):
        if project.date_end:
            return project.date_end.strftime("%d/%m/%Y")

    def get_folder_models(self, project):
        return {
            pk: FolderModelStatisticsSerializer(folder_model_stats).data
            for pk, folder_model_stats in project.folder_models_statistics.items()
        }

    def get_budget_tracking(self, project):
        return project.budget_summary

    def get_custom_display_fields(self, project):
        return project.custom_display_fields


class ExportStatisticsSerializer(ProjectStatisticsSerializer):
    is_actimmo = serpy.MethodField()

    def get_is_actimmo(self, project):
        return project.is_actimmo


class ExportActionsSerializer(ExportStatisticsSerializer):
    actions = serpy.MethodField()
    organizations = serpy.MethodField()
    contacts = serpy.MethodField()

    def get_actions(self, project):
        actions = []
        for folder_model_stats in project.folder_models_statistics.values():
            actions += list(folder_model_stats["actions_queryset"])
        actions.sort(key=lambda action: action.date)
        return ActionExportSerializer(actions, many=True).data

    def get_organizations(self, project):
        return project.organizations

    def get_contacts(self, project):
        return project.contacts

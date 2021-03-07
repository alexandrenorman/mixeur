import serpy

from fac.models import Project
from fac.serializers import FolderModelSimpleSerializer, PeriodSerializer

from helpers.serializers import AutoModelSerializer


class ProjectSerializer(AutoModelSerializer):
    model = Project
    exclude = ["groups", "type_valorizations"]

    periods = serpy.MethodField()
    folder_models = serpy.MethodField()
    groups = serpy.MethodField()

    def get_custom_form_data(self, obj):
        if obj.custom_form_data is None:
            return {}

        return obj.custom_form_data

    def get_periods(self, project):
        budgets_periods = [budget.period for budget in project.user_budgets]
        objectives_status_periods = [
            objective.period
            for folder_model in project.folder_models.all()
            for status in folder_model.statuses.all()
            for objective in status.user_status_objectives
        ]
        objectives_action_periods = [
            objective.period
            for folder_model in project.folder_models.all()
            for category in folder_model.categories.all()
            for action_model in category.action_models.all()
            for objective in action_model.user_action_objectives
        ]
        periods_pk = set()
        periods = []
        for period in (
            budgets_periods + objectives_status_periods + objectives_action_periods
        ):
            if period.pk not in periods_pk:
                periods_pk.add(period.pk)
                periods.append(period)
        return PeriodSerializer(periods, many=True).data

    def get_folder_models(self, project):
        return FolderModelSimpleSerializer(project.folder_models.all(), many=True).data

    def get_groups(self, project):
        budgets_groups = [budget.group for budget in project.user_budgets]
        objectives_status_groups = [
            objective.group
            for folder_model in project.folder_models.all()
            for status in folder_model.statuses.all()
            for objective in status.user_status_objectives
        ]
        objectives_action_groups = [
            objective.group
            for folder_model in project.folder_models.all()
            for category in folder_model.categories.all()
            for action_model in category.action_models.all()
            for objective in action_model.user_action_objectives
        ]
        groups_pk = set()
        groups = []
        for group in (
            budgets_groups + objectives_status_groups + objectives_action_groups
        ):
            if group.pk not in groups_pk:
                groups_pk.add(group.pk)
                groups.append(group)
        return [{"pk": group.pk, "name": group.name} for group in groups]

from datetime import datetime

from .project_view import get_query_params_groups
from helpers.views import ExpertRequiredApiView, ModelReadOnlyView

from fac.models import ActionModel
from fac.serializers import DidActionSerializer


class DidActionView(ModelReadOnlyView, ExpertRequiredApiView):
    """
    Get list of folders where an action has been done
    """

    model = ActionModel
    serializer = DidActionSerializer
    perm_module = "did_action"
    updated_at_attribute_name = "updated_at"

    def get_object(self, pk, request):
        date_start = None
        date_end = None
        if request.GET.get("date_start"):
            date_start = datetime.strptime(request.GET["date_start"], "%Y-%m-%d").date()
        if request.GET.get("date_end"):
            date_end = datetime.strptime(request.GET["date_end"], "%Y-%m-%d").date()

        groups_filter = get_query_params_groups(request)

        action_model = super().get_object(pk, request)

        all_folders = action_model.category_model.folder_model.folders.filter(
            owning_group__in=groups_filter
        ).prefetch_related("actions__model", "model__statuses__action_models")
        action_model.folders = [
            folder
            for folder in all_folders
            if [
                action
                for action in folder.actions.filter(model=action_model, done=True)
                if (date_start < action.date if date_start else True)
                and (action.date < date_end if date_end else True)
            ]
        ]

        return action_model

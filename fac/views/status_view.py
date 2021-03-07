from datetime import datetime

from .project_view import get_query_params_groups
from helpers.views import ExpertRequiredApiView, ModelReadOnlyView

from fac.models import Status
from fac.serializers import StatusSerializer


class StatusView(ModelReadOnlyView, ExpertRequiredApiView):
    """
    Status View
    """

    model = Status
    serializer = StatusSerializer
    perm_module = "fac/status"
    updated_at_attribute_name = "updated_at"

    def get_object(self, pk, request):
        date_end = None
        if request.GET.get("date_end"):
            date_end = datetime.strptime(request.GET["date_end"], "%Y-%m-%d").date()
        groups_filter = get_query_params_groups(request)

        status = super().get_object(pk, request)

        all_folders = status.folder_model.folders.filter(
            owning_group__in=groups_filter
        ).prefetch_related("actions__model", "model__statuses__action_models")
        status.status_folders = [
            folder for folder in all_folders if folder.get_status(date_end) == status
        ]

        return status

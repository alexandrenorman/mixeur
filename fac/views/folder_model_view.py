# -*- coding: utf-8 -*-
from helpers.views import ExpertRequiredApiView, ModelReadOnlyView

from fac.models import FolderModel
from fac.serializers import FolderModelSerializer


class FolderModelView(ModelReadOnlyView, ExpertRequiredApiView):
    """
    FolderModel View
    """

    model = FolderModel
    serializer = FolderModelSerializer
    perm_module = "foldermodel"
    updated_at_attribute_name = "updated_at"

    def filter(self, request, queryset):
        return (
            super()
            .filter(request, queryset)
            .accessible_by(request.user)
            .prefetch_related(
                "project", "categories__action_models__valorizations__type_valorization"
            )
        )

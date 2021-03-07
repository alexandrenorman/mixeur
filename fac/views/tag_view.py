# -*- coding: utf-8 -*-
from fac.forms import TagForm
from fac.models import Tag
from fac.serializers import SimpleTagSerializer, TagSerializer
from helpers.views import ExpertRequiredApiView, ModelView


class TagView(ModelView, ExpertRequiredApiView):
    """
    Tag View
    """

    model = Tag
    form = TagForm
    serializer = TagSerializer
    perm_module = "tag"

    def filter(self, request, queryset):
        return (
            super()
            .filter(request, queryset)
            .accessible_by(request.user)
            .prefetch_related(
                "contacts__owning_group",
                "contacts__referents",
                "contacts__tags",
                "contacts__client_account",
                "organizations__owning_group",
                "organizations__referents",
                "organizations__tags",
                "owning_group",
            )
        )

    def get_serializer(self, request, call):
        """
        Return simple tag serializer for listing
        """
        if call == "LIST":
            return SimpleTagSerializer
        return super().get_serializer(request, call)

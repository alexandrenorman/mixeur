# -*- coding: utf-8 -*-
from helpers.views import ModelReadOnlyView, ApiView

from newsletters.models import GroupOfNewsletters
from newsletters.serializers import GroupOfNewslettersPublicSerializer


class GroupOfNewslettersPublicView(ModelReadOnlyView, ApiView):
    """
    GroupOfNewsletters Public View
    """

    model = GroupOfNewsletters
    form = None
    serializer = GroupOfNewslettersPublicSerializer
    perm_module = "newsletters/groupofnewsletterspublic"
    updated_at_attribute_name = "updated_at_including_newsletters"

    def filter(self, request, queryset):
        """
        Filter queryset from request argument
        """
        slug = request.GET.get("slug")
        queryset = queryset.filter(is_active=True, is_public=True)

        if slug:
            queryset = queryset.filter(group__slug=slug)

        queryset = queryset.filter(
            pk__in=[x.pk for x in queryset.all() if x.has_published_newsletters]
        )

        return queryset

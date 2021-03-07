# -*- coding: utf-8 -*-
from helpers.views import ExpertRequiredApiView, ModelView

from newsletters.models import GroupOfNewsletters
from newsletters.forms import GroupOfNewslettersForm
from newsletters.serializers import GroupOfNewslettersSerializer


class GroupOfNewslettersView(ModelView, ExpertRequiredApiView):
    """
    GroupOfNewsletters View
    """

    model = GroupOfNewsletters
    form = GroupOfNewslettersForm
    serializer = GroupOfNewslettersSerializer
    perm_module = "newsletters/groupofnewsletters"
    updated_at_attribute_name = "updated_at_including_newsletters"

    def filter(self, request, queryset):
        """
        Filter queryset from request argument
        """
        slug = request.GET.get("slug")

        if slug:
            queryset = queryset.filter(group__name=slug)

        return queryset

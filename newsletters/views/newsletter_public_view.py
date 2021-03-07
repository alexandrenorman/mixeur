# -*- coding: utf-8 -*-
from helpers.views import ModelReadOnlyView, ApiView

from newsletters.models import Newsletter
from newsletters.serializers import NewsletterSerializer


class NewsletterPublicView(ModelReadOnlyView, ApiView):
    """
    Newsletter View
    """

    model = Newsletter
    form = None
    serializer = NewsletterSerializer
    perm_module = "newsletters/newsletter"
    perm_module = "newsletters/groupofnewsletterspublic"
    updated_at_attribute_name = "updated_at"

    def filter(self, request, queryset):
        """
        Filter queryset from request argument
        """
        slug = request.GET.get("slug")
        group_slug = request.GET.get("group_slug")

        if slug:
            queryset = queryset.filter(slug=slug)

        if group_slug:
            queryset = queryset.filter(group_of_newsletters__group__name=group_slug)

        newsletters_id = [x.pk for x in queryset.all() if x.is_active]

        return queryset.filter(pk__in=newsletters_id)

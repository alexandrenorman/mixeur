# -*- coding: utf-8 -*-
from helpers.views import ExpertRequiredApiView, ModelView

from newsletters.models import Newsletter
from newsletters.forms import NewsletterForm
from newsletters.serializers import NewsletterSerializer


class NewsletterView(ModelView, ExpertRequiredApiView):
    """
    Newsletter View
    """

    model = Newsletter
    form = NewsletterForm
    serializer = NewsletterSerializer
    perm_module = "newsletters/newsletter"

    def filter(self, request, queryset):
        if "group" in request.GET:
            queryset = queryset.filter(group_of_newsletters__pk=request.GET["group"])

        return queryset

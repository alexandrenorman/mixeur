# -*- coding: utf-8 -*-
from types import SimpleNamespace

from django.http import JsonResponse

from fac.models import Contact, Organization

from helpers.views import (
    AdvisorRequiredApiView,
)

from visit_report.models import Housing
from visit_report.serializers import EntitiesListSerializer


class EntitiesListView(AdvisorRequiredApiView):
    """"""

    def get(self, request, *args, **kwargs):
        selected_type = request.GET.get("type", None)

        results = SimpleNamespace()

        if not selected_type or selected_type == "contacts":
            contacts_pk_has_report = (
                Housing.objects.filter(
                    content_type__model="contact", groups=request.user.group
                )
                .order_by("-id")[:20]
                .values_list("contact_or_organization_id", flat=True)
            )
            results.contacts = Contact.objects.filter(pk__in=contacts_pk_has_report)

        if not selected_type or selected_type == "organizations":
            organizations_pk_has_report = (
                Housing.objects.filter(
                    content_type__model="organization", groups=request.user.group
                )
                .order_by("-id")[:20]
                .values_list("contact_or_organization_id", flat=True)
            )
            results.organizations = Organization.objects.filter(
                pk__in=organizations_pk_has_report
            )

        return JsonResponse(EntitiesListSerializer(results).data)

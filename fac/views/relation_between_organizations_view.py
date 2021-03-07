# -*- coding: utf-8 -*-
from fac.forms import RelationBetweenOrganizationForm
from fac.models import RelationBetweenOrganization
from fac.serializers import RelationBetweenOrganizationSerializer
from helpers.views import ExpertRequiredApiView, ModelView


class RelationBetweenOrganizationView(ModelView, ExpertRequiredApiView):
    """
    RelationBetweenOrganization View
    """

    model = RelationBetweenOrganization
    form = RelationBetweenOrganizationForm
    serializer = RelationBetweenOrganizationSerializer
    perm_module = "relationbetweenorganization"

    def filter(self, request, queryset):
        return super().filter(request, queryset).accessible_by(request.user)

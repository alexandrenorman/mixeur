# -*- coding: utf-8 -*-
from fac.forms import MemberOfOrganizationForm
from fac.models import MemberOfOrganization, Tag
from fac.serializers import MemberOfOrganizationSerializer
from helpers.views import ExpertRequiredApiView, ModelView


class MemberOfOrganizationView(ModelView, ExpertRequiredApiView):
    """
    MemberOfOrganization View
    """

    model = MemberOfOrganization
    form = MemberOfOrganizationForm
    serializer = MemberOfOrganizationSerializer
    perm_module = "memberoforganization"

    def filter(self, request, queryset):
        if "organization" in request.GET:
            return queryset.filter(organization=request.GET["organization"])
        if "contact" in request.GET:
            return queryset.filter(contact=request.GET["contact"])
        return queryset

    def post_save(self, request, instance, member_organization_data, created):
        """
        Save object's M2M fields
        """
        self._save_m2m_from_select(
            instance=instance,
            attribute="tags",
            model_queryset=Tag.objects,
            data=member_organization_data.get("tags", []),
        )
        self._save_m2m_from_select(
            instance=instance,
            attribute="competencies_tags",
            model_queryset=Tag.objects,
            data=member_organization_data.get("competencies_tags", []),
        )

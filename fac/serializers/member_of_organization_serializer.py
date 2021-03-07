# -*- coding: utf-8 -*-
from fac.serializers.tag_select_serializer import TagSelectSerializer
from helpers.serializers import AutoModelSerializer
from fac.models import MemberOfOrganization
from .contact_serializer import ContactSerializer
from .organization_serializer import OrganizationSerializer


class MemberOfOrganizationSerializer(AutoModelSerializer):
    model = MemberOfOrganization

    def get_contact(self, obj):
        return ContactSerializer(obj.contact).data

    def get_organization(self, obj):
        return OrganizationSerializer(obj.organization).data

    def get_owning_group(self, obj):
        return obj.owning_group.pk

    def get_tags(self, obj):
        return TagSelectSerializer(obj.tags.all(), many=True).data

    def get_competencies_tags(self, obj):
        return TagSelectSerializer(obj.competencies_tags.all(), many=True).data

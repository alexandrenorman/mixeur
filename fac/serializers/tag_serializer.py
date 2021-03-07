# -*- coding: utf-8 -*-
from .contact_serializer import ContactSerializer
from .organization_serializer import OrganizationSerializer
from .simple_tag_serializer import SimpleTagSerializer


class TagSerializer(SimpleTagSerializer):
    def get_contacts(self, obj):
        return ContactSerializer(obj.contacts.all(), many=True).data

    def get_organizations(self, obj):
        return OrganizationSerializer(obj.organizations.all(), many=True).data

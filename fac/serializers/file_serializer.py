# -*- coding: utf-8 -*-
from fac.models import File, Contact, Organization
from helpers.serializers import AutoModelSerializer

from .contact_serializer import ContactSerializer
from .organization_serializer import OrganizationSerializer
from .tag_select_serializer import TagSelectSerializer


class FileSerializer(AutoModelSerializer):
    model = File

    exclude = [
        "content_type",
        "object_id",
        "linked_object",
        "action",
        "contact",
        "organization",
    ]

    def get_linked_object(self, obj):
        linked_object = obj.linked_object
        if type(linked_object) is Contact:
            return ContactSerializer(linked_object).data
        if type(linked_object) is Organization:
            return OrganizationSerializer(linked_object).data
        return ""

    def get_owning_group(self, obj):
        return obj.owning_group.pk

    def get_document(self, obj):
        if obj.document:
            return obj.document.url

    def get_tags(self, obj):
        return TagSelectSerializer(obj.tags.all(), many=True).data

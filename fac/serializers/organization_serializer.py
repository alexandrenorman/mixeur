# -*- coding: utf-8 -*-
from fac.models import Organization

from helpers.serializers import (
    AutoModelSerializer,
    FaxSerializerMixin,
    PhoneSerializerMixin,
)

from .tag_select_serializer import TagSelectSerializer
from .user_select_serializer import UserSelectSerializer


class OrganizationSerializer(
    AutoModelSerializer, PhoneSerializerMixin, FaxSerializerMixin
):
    exclude = ["files", "notes", "ecorenover_simulations"]
    model = Organization

    def get_custom_form_data(self, obj):
        if obj.custom_form_data is None:
            return {}

        return obj.custom_form_data

    def get_owning_group(self, obj):
        return obj.owning_group.pk

    def get_fileimport(self, obj):
        if obj.fileimport is not None:
            return obj.fileimport.pk
        else:
            return None

    def get_referents(self, obj):
        return UserSelectSerializer(obj.referents.all(), many=True).data

    def get_tags(self, obj):
        return TagSelectSerializer(obj.tags.all(), many=True).data

    def get_duration_by_project(self, obj):
        return obj.get_duration_by_project()

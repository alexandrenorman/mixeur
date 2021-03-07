# -*- coding: utf-8 -*-
import serpy

from .tag_select_serializer import TagSelectSerializer


class OrganizationDropdownListSerializer(serpy.Serializer):
    label = serpy.MethodField()
    value = serpy.MethodField()
    tags = serpy.MethodField()

    def get_label(self, obj):
        return obj.name.strip()

    def get_value(self, obj):
        return obj.pk

    def get_tags(self, obj):
        return TagSelectSerializer(obj.tags.all(), many=True).data

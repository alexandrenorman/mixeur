# -*- coding: utf-8 -*-
import serpy

from .tag_select_serializer import TagSelectSerializer


class ContactDropdownListSerializer(serpy.Serializer):
    label = serpy.MethodField()
    value = serpy.MethodField()
    tags = serpy.MethodField()

    def get_label(self, obj):
        if obj.email:
            return f"{obj.full_name.strip()} ({obj.email})"
        else:
            return obj.full_name.strip()

    def get_value(self, obj):
        return obj.pk

    def get_tags(self, obj):
        return TagSelectSerializer(obj.tags.all(), many=True).data

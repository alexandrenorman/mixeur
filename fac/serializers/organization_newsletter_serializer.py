# -*- coding: utf-8 -*-
import serpy

from .tag_select_serializer import TagSelectSerializer


class OrganizationNewsletterSerializer(serpy.Serializer):
    label = serpy.MethodField()
    value = serpy.MethodField()
    accepts_newsletters = serpy.MethodField()
    tags = serpy.MethodField()

    def get_label(self, obj):
        return obj.name.strip()

    def get_value(self, obj):
        return obj.pk

    def get_accepts_newsletters(self, obj):
        return obj.accepts_newsletters

    def get_tags(self, obj):
        return TagSelectSerializer(obj.tags.all(), many=True).data

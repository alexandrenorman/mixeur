# -*- coding: utf-8 -*-
import serpy


class TagSelectSerializer(serpy.Serializer):
    value = serpy.MethodField()
    label = serpy.MethodField()

    def get_value(self, tag):
        return tag.pk

    def get_label(self, tag):
        return tag.name

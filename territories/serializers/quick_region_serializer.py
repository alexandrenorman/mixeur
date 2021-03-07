# -*- coding: utf-8 -*-

import serpy


class QuickCommuneSerializer(serpy.Serializer):
    label = serpy.MethodField()
    value = serpy.MethodField()
    # children = serpy.MethodField()

    def get_label(self, obj):
        return obj.name

    def get_value(self, obj):
        return obj.pk

    # def get_children(self, obj):
    #     children = obj.commune_set.all()
    #     return QuickCommuneSerializer(children, many=True).data


class QuickDepartementSerializer(serpy.Serializer):
    label = serpy.MethodField()
    value = serpy.MethodField()
    children = serpy.MethodField()

    def get_label(self, obj):
        return obj.name

    def get_value(self, obj):
        return obj.pk

    def get_children(self, obj):
        children = obj.commune_set.all()
        return QuickCommuneSerializer(children, many=True).data


class QuickRegionSerializer(serpy.Serializer):
    label = serpy.MethodField()
    value = serpy.MethodField()
    children = serpy.MethodField()

    def get_label(self, obj):
        return obj.name

    def get_value(self, obj):
        return obj.pk

    def get_children(self, obj):
        children = obj.departement_set.all()
        return QuickDepartementSerializer(children, many=True).data

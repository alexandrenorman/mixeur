# -*- coding: utf-8 -*-

import serpy

from helpers.serializers import ModelSerializer, PhoneSerializerMixin
from accounts.serializers import GroupSimpleWithoutAdminGroupSerializer, UserSerializer


class PlaceSerializer(PhoneSerializerMixin, ModelSerializer):
    name = serpy.Field()
    slug = serpy.Field()
    groups = serpy.MethodField()
    selected_advisors = serpy.MethodField()
    presentation = serpy.Field()
    internal_presentation = serpy.Field()
    is_active = serpy.Field()
    address = serpy.Field()
    postcode = serpy.Field()
    inseecode = serpy.Field()
    img = serpy.MethodField()
    lat = serpy.Field()
    lon = serpy.Field()
    url = serpy.Field()
    color = serpy.Field()
    email = serpy.Field()

    def get_img(self, obj):
        if obj.img:
            return obj.img.url
        else:
            return None

    def get_groups(self, obj):
        groups = obj.groups.all()
        serializer = GroupSimpleWithoutAdminGroupSerializer(groups, many=True)
        return serializer.data

    def get_selected_advisors(self, obj):
        advisors = obj.selected_advisors.all()
        serializer = UserSerializer(advisors, many=True)
        return serializer.data


class PlaceSimpleSerializer(PhoneSerializerMixin, ModelSerializer):
    name = serpy.Field()
    slug = serpy.Field()
    presentation = serpy.Field()
    is_active = serpy.Field()
    address = serpy.Field()
    postcode = serpy.Field()
    inseecode = serpy.Field()
    lat = serpy.Field()
    lon = serpy.Field()
    url = serpy.Field()
    color = serpy.Field()
    email = serpy.Field()

    groups = serpy.MethodField()
    selected_advisors = serpy.MethodField()

    def get_groups(self, obj):
        return [x.pk for x in obj.groups.all()]

    def get_selected_advisors(self, obj):
        return [x.pk for x in obj.selected_advisors.all()]

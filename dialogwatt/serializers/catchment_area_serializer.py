# -*- coding: utf-8 -*-

import serpy

from accounts.serializers import GroupSimpleWithoutAdminGroupSerializer

from helpers.serializers import ModelSerializer


class CatchmentAreaSimpleSerializer(ModelSerializer):
    name = serpy.Field()


class CatchmentAreaSerializer(ModelSerializer):
    name = serpy.Field()
    is_active = serpy.Field()
    description = serpy.Field()
    group = GroupSimpleWithoutAdminGroupSerializer(required=False)
    territories = serpy.MethodField()
    additionnal_information = serpy.Field()

    def get_group(self, obj):
        group = obj.group.all()
        serializer = GroupSimpleWithoutAdminGroupSerializer(group)
        return serializer.data

    def get_territories(self, obj):
        communes = [x["pk"] for x in obj.territories.all().values("pk")]
        return communes

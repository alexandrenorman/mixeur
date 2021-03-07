# -*- coding: utf-8 -*-

import serpy

from helpers.serializers import PhoneSerializerMixin

# from .admin_group_simple_serializer import AdminGroupSimpleSerializer
from .user_simple_serializer import UserSimpleSerializer


class GroupSerializer(PhoneSerializerMixin, serpy.Serializer):
    pk = serpy.Field()
    name = serpy.Field()
    slug = serpy.Field()
    full_name = serpy.Field()
    display_name = serpy.MethodField()
    is_active = serpy.BoolField(required=False)
    is_admin = serpy.BoolField(required=False)
    date_joined = serpy.Field(required=False)
    users_count = serpy.Field()
    users = UserSimpleSerializer(required=False, many=True)
    # admin_group = AdminGroupSimpleSerializer(required=False)
    admin_group = serpy.MethodField()
    territories = serpy.MethodField(required=False)
    profile_pic = serpy.MethodField()
    presentation = serpy.Field(required=False)
    email = serpy.Field()
    address = serpy.Field()
    visible_fac_groups = serpy.MethodField()
    website = serpy.Field()

    def get_admin_group(self, obj):
        if obj.admin_group:
            return obj.admin_group.pk

        return None

    def get_profile_pic(self, obj):
        if obj.profile_pic:
            return obj.profile_pic.url
        else:
            return None

    def get_territories(self, obj):
        communes = [x["pk"] for x in obj.territories.all().values("pk")]
        return communes

    # def get_territories(self, obj):
    #     communes = obj.territories.all().values("pk", "name", "epci")
    #     json = [
    #         {"pk": x["pk"], "id": x["pk"], "name": x["name"], "epci": x["epci"]}
    #         for x in communes
    #     ]
    #     return json

    def get_visible_fac_groups(self, obj):
        laureates = [
            {"pk": group.pk, "name": group.name} for group in obj.laureate_groups.all()
        ]
        return laureates + [{"pk": obj.pk, "name": obj.name}]

    def get_display_name(self, obj):
        return obj.display_name

# -*- coding: utf-8 -*-

import serpy

from helpers.serializers import PhoneSerializerMixin
from .admin_group_simple_serializer import AdminGroupSimpleSerializer


class GroupSimpleSerializer(PhoneSerializerMixin, serpy.Serializer):
    pk = serpy.Field()
    name = serpy.Field()
    slug = serpy.Field()
    display_name = serpy.MethodField()
    is_active = serpy.BoolField(required=False)
    is_admin = serpy.BoolField(required=False)
    date_joined = serpy.Field(required=False)
    users_count = serpy.Field()
    admin_group = AdminGroupSimpleSerializer(required=False)
    profile_pic = serpy.MethodField()
    presentation = serpy.Field(required=False)
    email = serpy.Field()
    address = serpy.Field()
    website = serpy.Field()

    def get_profile_pic(self, obj):
        if obj.profile_pic:
            return obj.profile_pic.url
        else:
            return None

    def get_display_name(self, obj):
        return obj.display_name

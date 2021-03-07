# -*- coding: utf-8 -*-

import serpy

from helpers.serializers import PhoneSerializerMixin


class GroupSimpleWithoutAdminGroupSerializer(PhoneSerializerMixin, serpy.Serializer):
    pk = serpy.Field()
    name = serpy.Field()
    slug = serpy.Field()
    display_name = serpy.MethodField()
    is_active = serpy.BoolField(required=False)
    is_admin = serpy.BoolField(required=False)
    date_joined = serpy.Field(required=False)
    users_count = serpy.Field()
    users = serpy.MethodField()
    profile_pic = serpy.MethodField()
    presentation = serpy.Field(required=False)
    email = serpy.Field()
    address = serpy.Field()
    website = serpy.Field(required=False)

    def get_profile_pic(self, obj):
        if obj.profile_pic:
            return obj.profile_pic.url
        else:
            return None

    def get_users(self, obj):
        return [x.pk for x in obj.users]

    def get_display_name(self, obj):
        return obj.display_name

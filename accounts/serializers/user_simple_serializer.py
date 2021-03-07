# -*- coding: utf-8 -*-

import serpy
from helpers.serializers import PhoneSerializerMixin


class UserSimpleSerializer(PhoneSerializerMixin, serpy.Serializer):
    pk = serpy.Field()
    email = serpy.Field()
    first_name = serpy.Field()
    last_name = serpy.Field()
    user_type = serpy.Field()
    title = serpy.Field()
    color = serpy.Field()
    is_active = serpy.Field()
    profile_pic = serpy.MethodField()
    full_name = serpy.MethodField()
    name = serpy.MethodField()
    is_contact = serpy.MethodField()
    is_client = serpy.MethodField()

    def get_profile_pic(self, obj):
        if obj.profile_pic:
            return obj.profile_pic.url
        else:
            return None

    def get_full_name(self, obj):
        return obj.display_name

    def get_name(self, obj):
        return obj.display_name

    def get_is_contact(self, obj):
        return obj.is_contact

    def get_is_client(self, obj):
        return obj.is_client

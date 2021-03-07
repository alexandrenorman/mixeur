# -*- coding: utf-8 -*-

import serpy
from helpers.serializers import PhoneSerializerMixin
from .group_simple_serializer import GroupSimpleSerializer


class UserSerializer(PhoneSerializerMixin, serpy.Serializer):
    pk = serpy.Field()
    email = serpy.Field()
    first_name = serpy.Field()
    last_name = serpy.Field()
    user_type = serpy.Field()
    title = serpy.Field()
    color = serpy.Field()
    group = GroupSimpleSerializer(required=False)
    profile_pic = serpy.MethodField()
    full_name = serpy.MethodField()
    is_active = serpy.Field()
    civility = serpy.Field()

    def get_profile_pic(self, obj):
        if obj.profile_pic:
            return obj.profile_pic.url
        else:
            return None

    def get_full_name(self, obj):
        return obj.display_name

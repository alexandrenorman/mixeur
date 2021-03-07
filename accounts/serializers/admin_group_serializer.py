# -*- coding: utf-8 -*-
import serpy

from .user_simple_serializer import UserSimpleSerializer


class AdminGroupSerializer(serpy.Serializer):
    pk = serpy.Field()
    name = serpy.Field()
    is_active = serpy.BoolField(required=False)
    is_admin = serpy.BoolField(required=False)
    date_joined = serpy.Field(required=False)
    users_count = serpy.Field()
    users = UserSimpleSerializer(required=False, many=True)

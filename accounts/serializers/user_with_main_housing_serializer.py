# -*- coding: utf-8 -*-

import serpy

from helpers.serializers import PhoneSerializerMixin
from visit_report.serializers.housing_simple_serializer import HousingSimpleSerializer


class UserWithMainHousingSerializer(PhoneSerializerMixin, serpy.Serializer):
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
    main_housing = HousingSimpleSerializer(required=False)

    def get_profile_pic(self, obj):
        if obj.profile_pic:
            return obj.profile_pic.url
        else:
            return None

    def get_full_name(self, obj):
        return obj.display_name

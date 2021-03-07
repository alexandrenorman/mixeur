# -*- coding: utf-8 -*-

import serpy


class UserProfilePicSerializer(serpy.Serializer):
    pk = serpy.Field()
    profile_pic = serpy.MethodField()

    def get_profile_pic(self, obj):
        if obj.profile_pic:
            return obj.profile_pic.url
        else:
            return None

# -*- coding: utf-8 -*-

import serpy


class GroupReducedSerializer(serpy.Serializer):
    pk = serpy.Field()
    name = serpy.Field()
    display_name = serpy.MethodField()
    profile_pic = serpy.MethodField()
    website = serpy.Field()

    def get_profile_pic(self, obj):
        if obj.profile_pic:
            return obj.profile_pic.url
        else:
            return None

    def get_display_name(self, obj):
        return obj.display_name

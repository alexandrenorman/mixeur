# -*- coding: utf-8 -*-
import serpy


class UserSelectSerializer(serpy.Serializer):
    value = serpy.MethodField()
    label = serpy.MethodField()

    def get_value(self, user):
        return user.pk

    def get_label(self, user):
        return user.full_name

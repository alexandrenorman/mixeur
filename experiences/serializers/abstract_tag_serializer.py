# -*- coding: utf-8 -*-
from experiences.models import AbstractTag
from helpers.serializers import AutoModelSerializer


class AbstractTagSerializer(AutoModelSerializer):
    model = AbstractTag

    def get_owning_group(self, obj):
        """
        get field owning_group of type ForeignKey
        """
        if not obj.owning_group:
            return None

        return obj.owning_group.pk

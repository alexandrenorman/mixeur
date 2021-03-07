# -*- coding: utf-8 -*-
from helpers.serializers import AutoModelSerializer
from experiences.models import Explanation


class ExplanationSerializer(AutoModelSerializer):
    model = Explanation

    def get_owning_group(self, obj):
        """
        get field owning_group of type ForeignKey
        """
        return obj.owning_group.pk

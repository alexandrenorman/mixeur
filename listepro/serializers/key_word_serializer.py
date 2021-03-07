# -*- coding: utf-8 -*-
from helpers.serializers import AutoModelSerializer

from listepro.models import KeyWord


class KeyWordSerializer(AutoModelSerializer):
    model = KeyWord

    def get_category(self, obj):
        """
        get field category of type ForeignKey
        """
        return obj.category.pk

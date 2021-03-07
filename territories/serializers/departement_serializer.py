# -*- coding: utf-8 -*-
from helpers.serializers import AutoModelSerializer
from territories.models import Departement


class DepartementSerializer(AutoModelSerializer):
    model = Departement

    def get_region(self, obj):
        return obj.region.pk

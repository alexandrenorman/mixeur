# -*- coding: utf-8 -*-
from helpers.serializers import AutoModelSerializer
from territories.models import Region


class RegionSerializer(AutoModelSerializer):
    model = Region

# -*- coding: utf-8 -*-
from helpers.serializers import AutoModelSerializer

from listepro.models import Activity


class ActivitySerializer(AutoModelSerializer):
    model = Activity

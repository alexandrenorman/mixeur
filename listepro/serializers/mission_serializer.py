# -*- coding: utf-8 -*-
from helpers.serializers import AutoModelSerializer

from listepro.models import Mission


class MissionSerializer(AutoModelSerializer):
    model = Mission

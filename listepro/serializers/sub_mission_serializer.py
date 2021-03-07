# -*- coding: utf-8 -*-
from helpers.serializers import AutoModelSerializer

from listepro.models import SubMission


class SubMissionSerializer(AutoModelSerializer):
    model = SubMission

    def get_mission(self, obj):
        """
        get field mission of type ForeignKey
        """
        return obj.mission.pk

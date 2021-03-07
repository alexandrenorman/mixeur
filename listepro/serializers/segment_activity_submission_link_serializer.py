# -*- coding: utf-8 -*-
from helpers.serializers import AutoModelSerializer

from listepro.models import SegmentActivitySubMissionLink


class SegmentActivitySubMissionLinkSerializer(AutoModelSerializer):
    model = SegmentActivitySubMissionLink

    def get_segment(self, obj):
        """
        get field segment of type ForeignKey
        """
        return obj.segment.pk

    def get_activity(self, obj):
        """
        get field activity of type ForeignKey
        """
        return obj.activity.pk

    def get_sub_mission(self, obj):
        """
        get field sub_mission of type ForeignKey
        """
        return obj.sub_mission.pk

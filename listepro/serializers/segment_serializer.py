# -*- coding: utf-8 -*-
from helpers.serializers import AutoModelSerializer

from listepro.models import Segment


class SegmentSerializer(AutoModelSerializer):
    model = Segment

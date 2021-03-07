# -*- coding: utf-8 -*-
from helpers.serializers import AutoModelSerializer
from visit_report.models import Face


class FaceSerializer(AutoModelSerializer):
    model = Face

    def get_report(self, obj):
        return obj.report.pk

# -*- coding: utf-8 -*-
from helpers.serializers import AutoModelSerializer
from visit_report.models import WorkRecommendation


class WorkRecommendationSerializer(AutoModelSerializer):
    model = WorkRecommendation

    def get_report(self, obj):
        return obj.report.pk

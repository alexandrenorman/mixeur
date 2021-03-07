# -*- coding: utf-8 -*-
from helpers.serializers import AutoModelSerializer
from visit_report.models import ScenarioSummary


class ScenarioSummarySerializer(AutoModelSerializer):
    model = ScenarioSummary

    def get_scenario(self, obj):
        return obj.scenario.pk

# -*- coding: utf-8 -*-
from helpers.serializers import AutoModelSerializer
from visit_report.models import FinancialAid


class FinancialAidSerializer(AutoModelSerializer):
    model = FinancialAid

    def get_scenario(self, obj):
        return obj.scenario.pk

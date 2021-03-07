# -*- coding: utf-8 -*-
from helpers.serializers import AutoModelSerializer
from visit_report.models import Financing


class FinancingSerializer(AutoModelSerializer):
    model = Financing

    def get_scenario(self, obj):
        return obj.scenario.pk

# -*- coding: utf-8 -*-
from helpers.serializers import AutoModelSerializer
from visit_report.models import Scenario

from .financial_aid_serializer import FinancialAidSerializer
from .financing_serializer import FinancingSerializer
from .scenario_summary_serializer import ScenarioSummarySerializer


class ScenarioSerializer(AutoModelSerializer):
    model = Scenario

    def get_report(self, obj):
        return obj.report.pk

    def get_financial_aids(self, obj):
        objects = obj.financialaid_set.all()
        serializer = FinancialAidSerializer(objects, many=True)
        return serializer.data

    def get_financings(self, obj):
        objects = obj.financing_set.all()
        serializer = FinancingSerializer(objects, many=True)
        return serializer.data

    def get_scenario_summaries(self, obj):
        objects = obj.scenariosummary_set.all()
        serializer = ScenarioSummarySerializer(objects, many=True)
        return serializer.data

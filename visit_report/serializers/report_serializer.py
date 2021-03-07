# -*- coding: utf-8 -*-

from helpers.serializers import AutoModelSerializer

from visit_report.models import Report

from .face_serializer import FaceSerializer

# from .financial_aid_serializer import FinancialAidSerializer
# from .financing_serializer import FinancialSerializer
from .housing_serializer import HousingSerializer

# from .housing_simple_serializer import HousingSimpleSerializer
from .scenario_serializer import ScenarioSerializer

# from .scenario_summary_serializer import ScenarioSummarySerializer
from .step_serializer import StepSerializer
from .system_serializer import SystemSerializer
from .work_recommendation_serializer import WorkRecommendationSerializer
from .appendix_serializer import AppendixSerializer

from accounts.serializers import UserSimpleSerializer, GroupSimpleSerializer


# class ReportSimpleSerializer(AutoModelSerializer):
#     """
#     Report simple serializer
#     """
#
#     model = Report


class ReportSerializer(AutoModelSerializer):
    """
    Report serializer
    """

    model = Report

    def get_advisor(self, obj):
        if not obj.advisor:
            return None

        serializer = UserSimpleSerializer(obj.advisor)
        return serializer.data

    def get_group(self, obj):
        if not obj.group:
            return None

        serializer = GroupSimpleSerializer(obj.group)
        return serializer.data

    def get_housing(self, obj):
        serializer = HousingSerializer(obj.housing)
        return serializer.data

    def get_faces(self, obj):
        objects = obj.face.all()
        serializer = FaceSerializer(objects, many=True)
        return serializer.data

    def get_scenarios(self, obj):
        objects = obj.scenario.all()
        serializer = ScenarioSerializer(objects, many=True)
        return serializer.data

    def get_steps(self, obj):
        objects = obj.step.all()
        serializer = StepSerializer(objects, many=True)
        return serializer.data

    def get_systems(self, obj):
        objects = obj.system.all()
        serializer = SystemSerializer(objects, many=True)
        return serializer.data

    def get_work_recommendations(self, obj):
        objects = obj.work_recommendation.all()
        serializer = WorkRecommendationSerializer(objects, many=True)
        return serializer.data

    def get_appendix_table(self, obj):
        objects = obj.appendix.all()
        serializer = AppendixSerializer(objects, many=True)
        return serializer.data

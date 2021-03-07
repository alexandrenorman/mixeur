# -*- coding: utf-8 -*-
from helpers.serializers import AutoModelSerializer
from visit_report.models import Step


class StepSerializer(AutoModelSerializer):
    model = Step

    def get_report(self, obj):
        return obj.report.pk

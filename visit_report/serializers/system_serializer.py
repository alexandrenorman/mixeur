# -*- coding: utf-8 -*-
from helpers.serializers import AutoModelSerializer
from visit_report.models import System


class SystemSerializer(AutoModelSerializer):
    model = System

    def get_report(self, obj):
        return obj.report.pk

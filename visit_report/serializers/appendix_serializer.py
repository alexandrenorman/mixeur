# -*- coding: utf-8 -*-
from helpers.serializers import AutoModelSerializer
from visit_report.models import Appendix


class AppendixSerializer(AutoModelSerializer):
    model = Appendix

    def get_report(self, obj):
        """
        get field report of type ForeignKey
        """
        return obj.report.pk

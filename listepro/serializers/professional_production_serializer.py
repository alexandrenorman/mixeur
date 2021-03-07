# -*- coding: utf-8 -*-
from helpers.serializers import AutoModelSerializer

from listepro.models import ProfessionalProduction

from .calculation_method_serializer import CalculationMethodSerializer
from .usage_integrated_serializer import UsageIntegratedSerializer


class ProfessionalProductionSerializer(AutoModelSerializer):
    model = ProfessionalProduction

    def get_professional(self, obj):
        """
        get field professional of type ForeignKey
        """
        return obj.professional.pk

    def get_calculation_method(self, obj):
        """
        get field calculation_method of type ForeignKey
        """
        calculation_method = obj.calculation_method
        serializer = CalculationMethodSerializer(calculation_method)
        return serializer.data

    def get_usage_integrated(self, obj):
        """
        get field usage_integrated of type ManyToManyField
        """
        usage_integrated = obj.usage_integrated.all()
        serializer = UsageIntegratedSerializer(usage_integrated, many=True)
        return serializer.data

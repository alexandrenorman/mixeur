# -*- coding: utf-8 -*-
from helpers.serializers import AutoModelSerializer

from listepro.models import CalculationMethod


class CalculationMethodSerializer(AutoModelSerializer):
    model = CalculationMethod

# -*- coding: utf-8 -*-
from helpers.serializers import AutoModelSerializer
from energies.models import CarbonTax


class CarbonTaxSerializer(AutoModelSerializer):
    model = CarbonTax

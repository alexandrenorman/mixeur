# -*- coding: utf-8 -*-
from helpers.views import ApiView, ModelReadOnlyView

from energies.models import YearlyEnergyPrice

from energies.serializers import YearlyEnergyPriceSerializer


class YearlyEnergyPriceView(ModelReadOnlyView, ApiView):
    """
    YearlyEnergyPrice View
    """

    model = YearlyEnergyPrice

    serializer = YearlyEnergyPriceSerializer
    perm_module = "energies/yearlyenergyprice"
    updated_at_attribute_name = "updated_at"

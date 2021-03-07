# -*- coding: utf-8 -*-
from helpers.views import ApiView, ModelReadOnlyView

from energies.models import CarbonTax

from energies.serializers import CarbonTaxSerializer


class CarbonTaxView(ModelReadOnlyView, ApiView):
    """
    CarbonTax View
    """

    model = CarbonTax

    serializer = CarbonTaxSerializer
    perm_module = "energies/carbontax"
    updated_at_attribute_name = "updated_at"

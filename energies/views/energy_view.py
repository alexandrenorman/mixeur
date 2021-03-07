# -*- coding: utf-8 -*-
from helpers.views import ApiView, ModelReadOnlyView

from energies.models import Energy

from energies.serializers import EnergySerializer


class EnergyView(ModelReadOnlyView, ApiView):
    """
    Energy View
    """

    model = Energy

    serializer = EnergySerializer
    perm_module = "energies/energy"
    updated_at_attribute_name = "updated_at"

    def filter(self, request, queryset):
        return queryset.order_by("identifier").prefetch_related("yearly_energy_price")

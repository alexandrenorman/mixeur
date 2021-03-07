# -*- coding: utf-8 -*-
from helpers.views import ApiView, ModelReadOnlyView

from energies.models import EnergyVector

from energies.serializers import EnergyVectorSerializer


class EnergyVectorView(ModelReadOnlyView, ApiView):
    """
    EnergyVector View
    """

    model = EnergyVector

    serializer = EnergyVectorSerializer
    perm_module = "energies/energyvector"
    updated_at_attribute_name = "updated_at"

    def filter(self, request, queryset):
        return queryset.order_by("order").prefetch_related("energy")

# -*- coding: utf-8 -*-
from helpers.views import ApiView, ModelReadOnlyView

from energies.models import ProductionSystem

from energies.serializers import ProductionSystemSerializer


class ProductionSystemView(ModelReadOnlyView, ApiView):
    """
    ProductionSystem View
    """

    model = ProductionSystem

    serializer = ProductionSystemSerializer
    perm_module = "energies/productionsystem"
    updated_at_attribute_name = "updated_at"

    def filter(self, request, queryset):
        return queryset.order_by("identifier").prefetch_related("energy")

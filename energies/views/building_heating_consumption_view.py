# -*- coding: utf-8 -*-
from helpers.views import ApiView, ModelReadOnlyView

from energies.models import BuildingHeatingConsumption

from energies.serializers import BuildingHeatingConsumptionSerializer


class BuildingHeatingConsumptionView(ModelReadOnlyView, ApiView):
    """
    BuildingHeatingConsumption View
    """

    model = BuildingHeatingConsumption

    serializer = BuildingHeatingConsumptionSerializer
    perm_module = "energies/buildingheatingconsumption"
    updated_at_attribute_name = "updated_at"

    def filter(self, request, queryset):
        return queryset.order_by("order")

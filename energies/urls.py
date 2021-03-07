# -*- coding: utf-8 -*-
from django.conf.urls import url

from energies.views import (
    BuildingHeatingConsumptionView,
    CarbonTaxView,
    EnergyView,
    EnergyVectorView,
    ProductionSystemView,
    SecondaryEfficiencyView,
    YearlyEnergyPriceView,
)

app_name = "energies"

urlpatterns = [
    url(
        r"^building-heating-consumption/$",
        BuildingHeatingConsumptionView.as_view(),
        name="building_heating_consumption_list",
    ),
    url(
        r"^building-heating-consumption/(?P<pk>[^/.]+)/$",
        BuildingHeatingConsumptionView.as_view(),
        name="building_heating_consumption_detail",
    ),
    url(r"^carbon-tax/$", CarbonTaxView.as_view(), name="carbon_tax_list"),
    url(
        r"^carbon-tax/(?P<pk>[^/.]+)/$",
        CarbonTaxView.as_view(),
        name="carbon_tax_detail",
    ),
    url(r"^energy/$", EnergyView.as_view(), name="energy_list"),
    url(r"^energy/(?P<pk>[^/.]+)/$", EnergyView.as_view(), name="energy_detail"),
    url(r"^energy-vector/$", EnergyVectorView.as_view(), name="energy_vector_list"),
    url(
        r"^energy-vector/(?P<pk>[^/.]+)/$",
        EnergyVectorView.as_view(),
        name="energy_vector_detail",
    ),
    url(
        r"^production-system/$",
        ProductionSystemView.as_view(),
        name="production_system_list",
    ),
    url(
        r"^production-system/(?P<pk>[^/.]+)/$",
        ProductionSystemView.as_view(),
        name="production_system_detail",
    ),
    url(
        r"^secondary-efficiency/$",
        SecondaryEfficiencyView.as_view(),
        name="secondary_efficiency_list",
    ),
    url(
        r"^secondary-efficiency/(?P<pk>[^/.]+)/$",
        SecondaryEfficiencyView.as_view(),
        name="secondary_efficiency_detail",
    ),
    url(
        r"^yearly-energy-price/$",
        YearlyEnergyPriceView.as_view(),
        name="yearly_energy_price_list",
    ),
    url(
        r"^yearly-energy-price/(?P<pk>[^/.]+)/$",
        YearlyEnergyPriceView.as_view(),
        name="yearly_energy_price_detail",
    ),
]

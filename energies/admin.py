# -*- coding: utf-8 -*-
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from .models import Energy, YearlyEnergyPrice


@admin.register(Energy)
class EnergyAdmin(admin.ModelAdmin):
    list_display = [
        "identifier",
        "current_price_admin",
        "primary_energy_ratio",
        "ghg_ratio",
        "carbon_tax",
        "pci_ratio",
        "density_ratio",
    ]
    search_fields = ["identifier"]
    exclude = []

    def current_price_admin(self, obj):
        return obj.current_price

    current_price_admin.short_description = _("Prix courant")


@admin.register(YearlyEnergyPrice)
class YearlyEnergyPriceAdmin(admin.ModelAdmin):
    list_display = ["year", "energy", "price"]
    search_fields = ["year"]
    exclude = []
    list_filter = ("energy", "year")

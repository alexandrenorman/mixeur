# -*- coding: utf-8 -*-
from django.contrib import admin

from listepro.models import ProfessionalProduction


@admin.register(ProfessionalProduction)
class ProfessionalProductionAdmin(admin.ModelAdmin):
    base_model = ProfessionalProduction
    list_display = [
        "pk",
        "professional",
        "production_name",
        "place",
        "label",
        "year",
        "consumption_before",
        "consumption_after",
        "calculation_method",
        "history",
        "completed_mission",
        "thermal_envelope",
        "system",
        "airtightness_test_result",
        "other_information",
    ]
    exclude = []

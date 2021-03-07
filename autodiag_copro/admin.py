# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import AltitudeRatio, ClimaticZoneRatio


@admin.register(AltitudeRatio)
class AltitudeRatioAdmin(admin.ModelAdmin):
    list_display = ["altitude", "value"]
    search_fields = ["altitude"]
    exclude = []


@admin.register(ClimaticZoneRatio)
class ClimaticZoneRatioAdmin(admin.ModelAdmin):
    list_display = ["code", "name", "value"]
    search_fields = ["code", "name"]
    exclude = []

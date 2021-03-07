# -*- coding: utf-8 -*-
from django.contrib import admin

from listepro.models import CalculationMethod


@admin.register(CalculationMethod)
class CalculationMethodAdmin(admin.ModelAdmin):
    base_model = CalculationMethod
    list_display = [
        "pk",
        "name",
    ]
    exclude = []

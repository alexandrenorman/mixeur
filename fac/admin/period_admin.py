# -*- coding: utf-8 -*-
from django.contrib import admin

from ..models import Period


@admin.register(Period)
class PeriodAdmin(admin.ModelAdmin):
    base_model = Period
    exclude = []

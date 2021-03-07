# -*- coding: utf-8 -*-
from django.contrib import admin

from dialogwatt.models import CalendarPermanentUrl


@admin.register(CalendarPermanentUrl)
class CalendarPermanentUrlAdmin(admin.ModelAdmin):
    base_model = CalendarPermanentUrl
    list_display = ["pk", "user", "unique_id"]
    exclude = []

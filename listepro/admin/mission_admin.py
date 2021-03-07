# -*- coding: utf-8 -*-
from django.contrib import admin

from listepro.models import Mission


@admin.register(Mission)
class MissionAdmin(admin.ModelAdmin):
    base_model = Mission
    list_display = [
        "pk",
        "name",
    ]
    exclude = []

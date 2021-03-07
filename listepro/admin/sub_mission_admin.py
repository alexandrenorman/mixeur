# -*- coding: utf-8 -*-
from django.contrib import admin

from listepro.models import SubMission


@admin.register(SubMission)
class SubMissionAdmin(admin.ModelAdmin):
    base_model = SubMission
    list_display = [
        "pk",
        "mission",
        "name",
    ]
    exclude = []

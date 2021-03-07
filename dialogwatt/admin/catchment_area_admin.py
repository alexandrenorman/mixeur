# -*- coding: utf-8 -*-
from django.contrib import admin

from dialogwatt.models import CatchmentArea


@admin.register(CatchmentArea)
class CatchmentAreaAdmin(admin.ModelAdmin):
    base_model = CatchmentArea
    list_display = ["pk", "name", "group", "description", "additionnal_information"]
    exclude = []

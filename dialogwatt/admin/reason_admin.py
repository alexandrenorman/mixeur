# -*- coding: utf-8 -*-
from django.contrib import admin

from dialogwatt.models import Reason


@admin.register(Reason)
class ReasonAdmin(admin.ModelAdmin):
    base_model = Reason
    list_display = [
        "pk",
        "name",
        "color",
        "is_active",
        "duration",
        "group",
        "internal_description",
        "show_description",
        "description",
    ]
    exclude = []

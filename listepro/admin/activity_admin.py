# -*- coding: utf-8 -*-
from django.contrib import admin

from listepro.models import Activity


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    base_model = Activity
    list_display = [
        "pk",
        "name",
        "icon",
    ]
    exclude = []

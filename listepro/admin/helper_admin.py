# -*- coding: utf-8 -*-
from django.contrib import admin

from listepro.models import Helper


@admin.register(Helper)
class HelperAdmin(admin.ModelAdmin):
    base_model = Helper
    list_display = [
        "pk",
        "name",
    ]
    exclude = []

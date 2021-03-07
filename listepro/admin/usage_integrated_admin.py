# -*- coding: utf-8 -*-
from django.contrib import admin

from listepro.models import UsageIntegrated


@admin.register(UsageIntegrated)
class UsageIntegratedAdmin(admin.ModelAdmin):
    base_model = UsageIntegrated
    list_display = [
        "pk",
        "name",
    ]
    exclude = []

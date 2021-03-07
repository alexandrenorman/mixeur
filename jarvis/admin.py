# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import AllowedSender


@admin.register(AllowedSender)
class AllowedSenderAdmin(admin.ModelAdmin):
    list_display = [
        "group",
        "is_active",
        "email",
    ]

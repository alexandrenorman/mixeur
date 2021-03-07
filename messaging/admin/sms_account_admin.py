# -*- coding: utf-8 -*-
from django.contrib import admin

from messaging.models import SmsAccount


@admin.register(SmsAccount)
class SmsAccountAdmin(admin.ModelAdmin):
    base_model = SmsAccount
    list_display = [
        "pk",
        "account_type",
        "twilio_account",
        "twilio_token",
        "ovh_account",
        "ovh_login",
        "ovh_password",
        "group",
        "is_active",
        "monthly_limit",
        "phone",
    ]
    exclude = []
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "account_type",
                    "is_active",
                    "phone",
                    "monthly_limit",
                    "group",
                )
            },
        ),
        (
            "OVH",
            {
                # 'classes': ('collapse',),
                "fields": ("ovh_account", "ovh_login", "ovh_password")
            },
        ),
        (
            "Twilio",
            {
                # 'classes': ('collapse',),
                "fields": ("twilio_account", "twilio_token")
            },
        ),
    )

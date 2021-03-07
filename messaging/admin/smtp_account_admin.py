# -*- coding: utf-8 -*-
from django.contrib import admin

from messaging.models import SmtpAccount


@admin.register(SmtpAccount)
class SmtpAccountAdmin(admin.ModelAdmin):
    base_model = SmtpAccount
    list_display = ["pk", "group", "name", "is_active", "smtp_type"]
    exclude = []
    fieldsets = (
        (
            None,
            {"fields": ("name", "is_active", "group", "from_username", "smtp_type")},
        ),
        (
            "SMTP",
            {
                # 'classes': ('collapse',),
                "fields": (
                    "email_host",
                    "email_port",
                    "email_host_user",
                    "email_host_password",
                    "email_use_tls",
                    "email_use_ssl",
                )
            },
        ),
        (
            "Mailgun",
            {
                # 'classes': ('collapse',),
                "fields": ("mailgun_apikey", "mailgun_monthly_limit")
            },
        ),
    )

# -*- coding: utf-8 -*-
from django.contrib import admin

from dialogwatt.models import ExchangeAttachment


@admin.register(ExchangeAttachment)
class ExchangeAttachmentAdmin(admin.ModelAdmin):
    base_model = ExchangeAttachment
    list_display = ["pk", "filecontent"]
    exclude = []

# -*- coding: utf-8 -*-
from django.contrib import admin

from fac.models import Action


@admin.register(Action)
class ActionAdmin(admin.ModelAdmin):
    base_model = Action
    list_display = [
        "pk",
        "duration",
        "date",
        "done",
        "message",
        "folder",
        "model",
        "valorization",
    ]
    exclude = []

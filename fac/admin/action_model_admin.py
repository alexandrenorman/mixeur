# -*- coding: utf-8 -*-
from django.contrib import admin

from fac.models import ActionModel


@admin.register(ActionModel)
class ActionModelAdmin(admin.ModelAdmin):
    base_model = ActionModel
    list_display = [
        "pk",
        "name",
        "category_model",
        "trigger_status",
    ]
    exclude = []
    list_filter = ("category_model", "category_model__folder_model")
    search_fields = ("name",)

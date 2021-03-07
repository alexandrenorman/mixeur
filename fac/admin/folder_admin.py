# -*- coding: utf-8 -*-
from django.contrib import admin

from fac.models import Folder


@admin.register(Folder)
class FolderAdmin(admin.ModelAdmin):
    base_model = Folder
    list_display = [
        "pk",
        "description",
        "linked_object",
        "model",
        "owning_group",
        "type_valorization",
    ]
    exclude = []

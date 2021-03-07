# -*- coding: utf-8 -*-
from django.contrib import admin

from nested_admin import NestedModelAdmin

from ..models import FolderModel

from .status_inline_admin import StatusInlineAdmin
from .category_model_inline_admin import CategoryModelInlineAdmin


@admin.register(FolderModel)
class FolderModelAdmin(NestedModelAdmin):
    inlines = [StatusInlineAdmin, CategoryModelInlineAdmin]
    list_display = ["pk", "name", "project", "icon"]
    exclude = []
    model = FolderModel

# -*- coding: utf-8 -*-
from django.contrib import admin

from fac.models import CategoryModel


@admin.register(CategoryModel)
class CategoryModelAdmin(admin.ModelAdmin):
    list_display = ["pk", "name", "folder_model"]
    exclude = []

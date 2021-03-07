# -*- coding: utf-8 -*-
from django.contrib import admin

from newsletters.models import Image


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    base_model = Image
    list_display = ["pk", "newsletter", "image"]
    exclude = []

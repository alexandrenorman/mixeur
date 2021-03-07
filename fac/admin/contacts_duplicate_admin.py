# -*- coding: utf-8 -*-
from django.contrib import admin

from ..models import ContactsDuplicate


@admin.register(ContactsDuplicate)
class ContactsDuplicateAdmin(admin.ModelAdmin):
    list_display = ["pk", "acknowledged", "created_at"]
    exclude = []

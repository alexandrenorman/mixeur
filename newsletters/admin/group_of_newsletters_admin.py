# -*- coding: utf-8 -*-
from django.contrib import admin

from newsletters.models import GroupOfNewsletters


@admin.register(GroupOfNewsletters)
class GroupOfNewslettersAdmin(admin.ModelAdmin):
    base_model = GroupOfNewsletters
    list_display = [
        "pk",
        "group",
        "slug",
        "title",
        "is_active",
        "is_public",
        "header",
        "header_link",
        "footer",
        "footer_link",
        "description",
    ]
    exclude = []

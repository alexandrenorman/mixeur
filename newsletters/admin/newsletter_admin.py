# -*- coding: utf-8 -*-
from django.contrib import admin

from newsletters.models import Newsletter


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    base_model = Newsletter
    list_display = [
        "pk",
        "group_of_newsletters",
        "slug",
        "title",
        "is_active",
        "is_public",
        "publication_start_date",
        "publication_end_date",
        "description",
    ]
    exclude = []

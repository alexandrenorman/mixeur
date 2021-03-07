from django.contrib import admin

from fac.models import Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ["pk", "name", "description", "owning_group"]
    list_filter = ("owning_group__name",)
    search_fields = ("name",)
    exclude = []

from django.contrib import admin

from fac.models import File


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = ["pk", "linked_object", "document", "created_at", "note"]
    search_fields = ("linked_object", "note", "tags")
    exclude = []

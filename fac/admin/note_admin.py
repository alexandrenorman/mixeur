from django.contrib import admin

from fac.models import Note


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ["pk", "linked_object", "created_at", "note"]
    search_fields = ("linked_object", "note", "tags")
    exclude = []

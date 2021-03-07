from django.contrib import admin

from fac.models import List


@admin.register(List)
class ListAdmin(admin.ModelAdmin):
    list_display = ["title", "nb_contacts"]
    search_fields = ("title",)
    exclude = []
    readonly_fields = ["nb_contacts"]

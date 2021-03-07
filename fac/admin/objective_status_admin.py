from django.contrib import admin

from fac.models import ObjectiveStatus


@admin.register(ObjectiveStatus)
class ObjectiveStatusAdmin(admin.ModelAdmin):
    list_display = ["pk", "name", "period", "group", "status", "nb_statuses"]
    exclude = []

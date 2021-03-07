from django.contrib import admin

from fac.models import EcorenoverSimulation


@admin.register(EcorenoverSimulation)
class EcorenoverSimulationAdmin(admin.ModelAdmin):
    list_display = ["pk", "linked_object", "description", "updated_at"]
    search_fields = ("linked_object", "description")
    exclude = []

from django.contrib import admin

from fac.forms import ObjectiveActionsAdminForm
from fac.models import ObjectiveAction


@admin.register(ObjectiveAction)
class ObjectiveActionAdmin(admin.ModelAdmin):
    list_display = ["pk", "name", "period", "group", "model_action", "nb_actions"]
    exclude = []

    form = ObjectiveActionsAdminForm

from django.contrib import admin

from fac.models import Budget


@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ["pk", "group", "period", "project"]
    list_filter = ("group__name",)
    exclude = []

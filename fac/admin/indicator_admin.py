from django.contrib import admin

from fac.models import Indicator


@admin.register(Indicator)
class IndicatorAdmin(admin.ModelAdmin):
    exclude = []

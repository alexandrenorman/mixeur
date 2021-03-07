from django.contrib import admin

from .models import (
    Face,
    FinancialAid,
    Financing,
    Housing,
    Report,
    ScenarioSummary,
    Scenario,
    Step,
    System,
    WorkRecommendation,
    Appendix,
)


class ReportAdmin(admin.ModelAdmin):
    base_model = Report
    list_display = ["pk", "housing", "advisor", "group"]
    list_filter = ("advisor", "group")
    search_fields = ("housing", "advisor", "group")


class HousingAdmin(admin.ModelAdmin):
    base_model = Housing
    list_display = ["pk", "address", "housing_groups", "contact_entity"]
    search_fields = ["contact_entity"]

    def housing_groups(self, inst):
        return ",".join([group.name for group in inst.groups.all()])


admin.site.register(Face)
admin.site.register(FinancialAid)
admin.site.register(Financing)
admin.site.register(Housing, HousingAdmin)
admin.site.register(Report, ReportAdmin)
admin.site.register(ScenarioSummary)
admin.site.register(Scenario)
admin.site.register(Step)
admin.site.register(System)
admin.site.register(WorkRecommendation)
admin.site.register(Appendix)

from django.contrib import admin

from fac.models import MemberOfOrganization


@admin.register(MemberOfOrganization)
class MemberOfOrganizationAdmin(admin.ModelAdmin):
    list_display = ["contact", "organization", "title_in_organization"]
    list_filter = ("organization__name", "owning_group__name")
    search_fields = (
        "contact__first_name",
        "contact__last_name",
        "contact__email",
        "organization__name",
    )
    exclude = []

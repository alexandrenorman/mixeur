from django.contrib import admin

from django.utils.translation import ugettext_lazy as _
from fac.models import RelationBetweenOrganization


@admin.register(RelationBetweenOrganization)
class RelationBetweenOrganizationAdmin(admin.ModelAdmin):
    list_display = [
        "pk",
        "display_name",
        "first_organization",
        "relation_name",
        "second_organization",
    ]
    exclude = []

    def display_name(self, obj):
        return str(obj)

    display_name.short_description = _("Nom")

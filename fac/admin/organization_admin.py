from django.contrib import admin

from .member_of_organization_inline_admin import MembersOfOrganizationInline
from .note_inline_admin import NoteInline
from fac.models import Organization


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ["pk", "name"]
    list_filter = ("owning_group__name",)
    search_fields = ("name",)
    exclude = []
    inlines = [MembersOfOrganizationInline, NoteInline]

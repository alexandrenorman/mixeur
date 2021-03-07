from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from .member_of_organization_inline_admin import MembersOfOrganizationInline
from .note_inline_admin import NoteInline
from fac.models import Contact


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = [
        "pk",
        "first_name",
        "last_name",
        "email",
        "ctags",
        "phplist",
        "updated_at",
    ]
    list_filter = ("blacklisted", "confirmed", "owning_group__name")
    search_fields = ("first_name", "last_name", "email", "tags__name")
    readonly_fields = ["blacklisted", "confirmed"]
    exclude = []
    inlines = [MembersOfOrganizationInline, NoteInline]

    def ctags(self, obj):
        return ", ".join([str(x) for x in obj.tags.all()])

    ctags.short_description = _("Tags")

    def phplist(self, obj):
        return not obj.blacklisted and obj.confirmed

    phplist.short_description = _("Valide dans PhpList")
    phplist.boolean = True

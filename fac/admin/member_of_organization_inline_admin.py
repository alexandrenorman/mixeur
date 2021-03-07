# -*- coding: utf-8 -*-
from django.contrib import admin

from fac.models import MemberOfOrganization


class MembersOfOrganizationInline(admin.TabularInline):
    model = MemberOfOrganization
    extra = 0
    exclude = []
    readonly_fields = ["contact", "title_in_organization"]
    show_change_link = True

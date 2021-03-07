# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.postgres.fields import JSONField

from jsoneditor.forms import JSONEditor

from fac.models import Project

from .forms import ProjectAdminForm


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ["pk", "name", "get_groups"]
    exclude = []
    form = ProjectAdminForm
    formfield_overrides = {
        JSONField: {"widget": JSONEditor},
    }

    def get_groups(self, project):
        return ", ".join([group.name for group in project.groups.all()])

# -*- coding: utf-8 -*-
from django import forms
from django.contrib import admin
from django.contrib.postgres.fields import JSONField

from jsoneditor.forms import JSONEditor

from accounts.models import Group

from custom_forms.models import CustomForm

from fac.models import ActionModel, FolderModel, Project


def duplicate_custom_form(modeladmin, request, queryset):
    for obj in queryset:
        src = CustomForm.objects.get(pk=obj.pk)
        obj.pk = None
        # TODO: version will break if already exists
        obj.version += 1
        obj.save()
        dst = CustomForm.objects.get(pk=obj.pk)
        dst.projects.add(*src.projects.all())
        dst.groups.add(*src.groups.all())
        dst.folder_models.add(*src.folder_models.all())
        dst.action_models.add(*src.action_models.all())


duplicate_custom_form.short_description = "Dupliquer le formulaire"


class CustomFormAdminForm(forms.ModelForm):
    class Meta:
        model = CustomForm
        exclude = []

    projects = forms.ModelMultipleChoiceField(
        queryset=Project.objects.order_by("name"), required=False
    )
    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.order_by("name"), required=False
    )
    folder_models = forms.ModelMultipleChoiceField(
        queryset=FolderModel.objects.order_by("name"), required=False
    )
    action_models = forms.ModelMultipleChoiceField(
        queryset=ActionModel.objects.order_by(
            "category_model__folder_model__name", "name"
        ),
        required=False,
    )


@admin.register(CustomForm)
class CustomFormAdmin(admin.ModelAdmin):
    base_model = CustomForm
    form = CustomFormAdminForm
    formfield_overrides = {
        JSONField: {"widget": JSONEditor},
    }
    list_display = [
        "pk",
        "description",
        "model",
        "anchor",
        "version",
    ]
    exclude = []
    search_fields = (
        "description",
        "model",
        "anchor",
        "groups__name",
        "projects__name",
        "folder_models__name",
        "action_models__name",
    )
    list_filter = (
        "model",
        "anchor",
        "groups",
        "projects",
        "folder_models",
        "action_models",
    )

    actions = [
        duplicate_custom_form,
    ]

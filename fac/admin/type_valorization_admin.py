# -*- coding: utf-8 -*-
from django import forms
from django.contrib import admin

from accounts.models import Group

from ..models import TypeValorization


class ValorizationAdminForm(forms.ModelForm):
    class Meta:
        model = TypeValorization
        exclude = []

    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.order_by("name"), required=False
    )


@admin.register(TypeValorization)
class TypeValorizationAdmin(admin.ModelAdmin):
    base_model = TypeValorization
    form = ValorizationAdminForm

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)

        for project in form.instance.type_valorization_projects.all():
            for group in form.instance.groups.all():
                project.groups.add(group)

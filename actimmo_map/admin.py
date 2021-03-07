# -*- coding: utf-8 -*-
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from .models import ActimmoMap, ActimmoContact
from accounts.models import Group
from django import forms


class ActimmoMapForm(forms.ModelForm):
    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all().order_by("name")
    )

    class Meta:
        model = ActimmoMap
        exclude = []


class ActimmoContactForm(forms.ModelForm):
    group = forms.ModelChoiceField(queryset=Group.objects.all().order_by("name"))

    class Meta:
        model = ActimmoContact
        exclude = []


@admin.register(ActimmoMap)
class ActimmoMapAdmin(admin.ModelAdmin):
    list_display = ["department", "groups_list"]
    # exclude = ["groups"]
    exclude = []
    form = ActimmoMapForm

    def groups_list(self, obj):
        return ", ".join([x.name for x in obj.groups.all().order_by("name")])

    groups_list.short_description = _("Groupes")


@admin.register(ActimmoContact)
class ActimmoContactAdmin(admin.ModelAdmin):
    list_display = ["group", "email", "first_name", "last_name"]
    exclude = []
    form = ActimmoContactForm

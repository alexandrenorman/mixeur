# -*- coding: utf-8 -*-
from django import forms

from accounts.models import Group
from visit_report.models import Housing

from fac.forms import OrganizationOrContactField


class HousingForm(forms.ModelForm):
    """
    HousingForm

    Wait for an extra group argument (pk of Group) and on save
    add it to the Housing.groups set.
    """

    class Meta:
        model = Housing
        exclude = ["created_at", "updated_at", "groups"]

    is_main_address = forms.BooleanField(required=False)
    occupants_number = forms.IntegerField(required=False)
    ownership = forms.CharField(required=False)
    group = forms.IntegerField(required=False)
    contact_entity = OrganizationOrContactField()

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.contact_entity = self.cleaned_data["contact_entity"]

        instance.save()
        if "group" in self.data and self.data["group"] is not None:
            group = Group.objects.get(pk=self.data["group"])
            instance.groups.add(group)
        return instance

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data["group"] is not None:
            group_id = cleaned_data.pop("group")
            Group.objects.get(pk=group_id)

        return cleaned_data

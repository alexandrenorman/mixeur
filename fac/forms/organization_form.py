# -*- coding: utf-8 -*-
from django import forms
from fac.models import Organization
from helpers.forms import SelectToCharField


class OrganizationForm(forms.ModelForm):
    class Meta:
        model = Organization
        exclude = ["created_at", "updated_at", "tags", "referents"]

        type_of_organization = SelectToCharField()

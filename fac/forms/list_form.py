# -*- coding: utf-8 -*-
from django import forms
from fac.models import List


class ListForm(forms.ModelForm):
    class Meta:
        model = List
        exclude = [
            "created_at",
            "updated_at",
            "tags",
            "contacts",
            "organizations",
            "lists",
        ]

    use_organizations_as_contacts = forms.BooleanField(required=False)

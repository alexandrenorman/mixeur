# -*- coding: utf-8 -*-
from django import forms

from fac.models import RelationBetweenOrganization


class RelationBetweenOrganizationForm(forms.ModelForm):
    class Meta:
        model = RelationBetweenOrganization
        exclude = ["created_at", "updated_at"]

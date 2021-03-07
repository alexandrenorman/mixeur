# -*- coding: utf-8 -*-
from django import forms
from fac.models import MemberOfOrganization


class MemberOfOrganizationForm(forms.ModelForm):
    class Meta:
        model = MemberOfOrganization
        exclude = ["created_at", "updated_at", "tags", "competencies_tags"]

    use_address_from_organization = forms.BooleanField(required=False)

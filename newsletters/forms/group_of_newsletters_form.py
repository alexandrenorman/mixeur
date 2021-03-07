# -*- coding: utf-8 -*-
from django import forms

from newsletters.models import GroupOfNewsletters


class GroupOfNewslettersForm(forms.ModelForm):
    class Meta:
        model = GroupOfNewsletters
        exclude = ["created_at", "updated_at"]

    is_active = forms.BooleanField(required=False)

    is_public = forms.BooleanField(required=False)

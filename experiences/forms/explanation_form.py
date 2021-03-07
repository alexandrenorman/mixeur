# -*- coding: utf-8 -*-
from django import forms

from experiences.models import Explanation


class ExplanationForm(forms.ModelForm):
    class Meta:
        model = Explanation
        exclude = ["created_at", "updated_at"]

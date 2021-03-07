# -*- coding: utf-8 -*-
from django import forms

from visit_report.models import Step


class StepForm(forms.ModelForm):
    class Meta:
        model = Step
        exclude = ["created_at", "updated_at"]

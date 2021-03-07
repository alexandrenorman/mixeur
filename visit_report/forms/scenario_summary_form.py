# -*- coding: utf-8 -*-
from django import forms

from visit_report.models import ScenarioSummary


class ScenarioSummaryForm(forms.ModelForm):
    class Meta:
        model = ScenarioSummary
        exclude = ["created_at", "updated_at"]

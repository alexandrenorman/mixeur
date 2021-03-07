# -*- coding: utf-8 -*-
from django import forms

from visit_report.models import WorkRecommendation


class WorkRecommendationForm(forms.ModelForm):
    class Meta:
        model = WorkRecommendation
        exclude = ["created_at", "updated_at"]

    selected = forms.BooleanField(required=False)

    selected_scenario_secondary = forms.BooleanField(required=False)

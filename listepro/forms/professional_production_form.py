# -*- coding: utf-8 -*-
from django import forms

from helpers.forms import FullModelChoiceField

from listepro.models import CalculationMethod
from listepro.models import ProfessionalProduction


class ProfessionalProductionForm(forms.ModelForm):
    class Meta:
        model = ProfessionalProduction
        exclude = [
            "created_at",
            "updated_at",
            "usage_integrated",
        ]

    calculation_method = FullModelChoiceField(
        queryset=CalculationMethod.objects,
        required=True,
        to_field_name="pk",
    )

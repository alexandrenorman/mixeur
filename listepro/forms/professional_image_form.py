# -*- coding: utf-8 -*-
from django import forms

from helpers.forms import FullModelChoiceField

from listepro.models import ProfessionalImage
from listepro.models import ProfessionalProduction


class ProfessionalImageForm(forms.ModelForm):
    class Meta:
        model = ProfessionalImage
        exclude = ["created_at", "updated_at"]

    production = FullModelChoiceField(
        queryset=ProfessionalProduction.objects,
        required=True,
        to_field_name="pk",
    )

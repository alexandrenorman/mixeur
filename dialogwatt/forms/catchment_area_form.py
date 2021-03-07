# -*- coding: utf-8 -*-
from django import forms

from dialogwatt.models import CatchmentArea


class CatchmentAreaForm(forms.ModelForm):
    class Meta:
        model = CatchmentArea
        fields = (
            "name",
            "is_active",
            "group",
            "description",
            "additionnal_information",
        )

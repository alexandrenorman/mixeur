# -*- coding: utf-8 -*-
from django import forms

from dialogwatt.models import Reason
from territories.models import Commune


class FindPlacesFromInseecodeForm(forms.Form):
    inseecode = forms.ModelChoiceField(
        queryset=Commune.objects.all(),
        to_field_name="inseecode",
        required=True,
        empty_label=None,
    )
    reason = forms.ModelChoiceField(
        queryset=Reason.active.all(), required=True, empty_label=None
    )

# -*- coding: utf-8 -*-
from django import forms
from dialogwatt.models import Slot
from helpers.forms import ISODateTimeField, ListOfValuesField


class SlotDuplicateToDatesForm(forms.Form):
    slot = forms.ModelChoiceField(
        queryset=Slot.objects.exclude(status="cancelled"), required=True
    )
    dates = ListOfValuesField(ISODateTimeField, required=True)

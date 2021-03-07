# -*- coding: utf-8 -*-
from django import forms

from helpers.forms import ISODateTimeField

from dialogwatt.models import Reason, Place
from accounts.models import User
from territories.models import Commune

from django.utils.translation import ugettext_lazy as _


class FindAppointmentForm(forms.Form):
    reason = forms.ModelChoiceField(queryset=Reason.objects.all(), required=True)
    inseecode = forms.ModelChoiceField(
        queryset=Commune.objects.all(), to_field_name="inseecode", required=False
    )
    start_date = ISODateTimeField(required=False)
    advisor = forms.ModelChoiceField(queryset=User.advisors.all(), required=False)
    place = forms.ModelChoiceField(queryset=Place.objects.all(), required=False)

    def clean(self):
        """
        Verifies that at least one location exists (inseecode or place)
        """
        super().clean()
        if "inseecode" not in self.cleaned_data and "place" not in self.cleaned_data:
            raise forms.ValidationError(
                _(
                    "Il faut au moins une indication de lieu. Merci de remplir le lieu ou le code INSEE."
                )
            )
        return self.cleaned_data

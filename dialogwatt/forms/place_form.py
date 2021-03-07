# -*- coding: utf-8 -*-
from django import forms

from dialogwatt.models import Place


class PlaceForm(forms.ModelForm):
    class Meta:
        model = Place
        fields = (
            "name",
            "slug",
            # "groups",
            # "selected_advisors",
            "presentation",
            "internal_presentation",
            "phone",
            "email",
            "is_active",
            "address",
            "inseecode",
            "postcode",
            "lat",
            "lon",
            "url",
            "color",
        )

    is_active = forms.BooleanField(required=False)
    url = forms.URLField(required=False)

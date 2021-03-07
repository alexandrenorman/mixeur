# -*- coding: utf-8 -*-
from django import forms
from dialogwatt.models import CalendarPermanentUrl
from accounts.models import User

# from django.core.exceptions import ValidationError


class CalendarPermanentUrlForm(forms.ModelForm):
    class Meta:
        model = CalendarPermanentUrl
        fields = (
            # "created_at",
            # "updated_at",
            "user",
            # "advisors",
            # "places",
        )

    user = forms.ModelChoiceField(
        queryset=User.objects.filter(user_type__in=["superadvisor", "advisor"])
    )
    # def clean(self):
    #     super().clean()
    #     advisors = self.cleaned_data.get("advisors")
    #     places = self.cleaned_data.get("places")
    #     return self.cleaned_data

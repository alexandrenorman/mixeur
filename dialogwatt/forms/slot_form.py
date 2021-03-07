# -*- coding: utf-8 -*-
from django import forms
from dialogwatt.models import Slot
from helpers.forms import ISODateTimeField


class SlotForm(forms.ModelForm):
    class Meta:
        model = Slot
        fields = (
            "text",
            "group",
            # "recurrences",
            "start_date",
            "end_date",
            "visibility",
            "place",
            "catchment_area",
            "deadline",
            "time_between_slots",
            "use_advisor_calendar",
            "number_of_active_advisors",
            # "advisors",
            "description",
            "public_description",
            "status",
        )

    use_advisor_calendar = forms.BooleanField(required=False)
    start_date = ISODateTimeField(required=True)
    end_date = ISODateTimeField(required=True)

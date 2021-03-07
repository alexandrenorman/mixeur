# -*- coding: utf-8 -*-
from django import forms

from accounts.models import User

from helpers.forms import FullModelChoiceField

from listepro.models import Activity, Job, Professional


class ActivityRadioSelect(forms.widgets.RadioSelect):
    template_name = "widgets/radio.html"


class ProfessionalForm(forms.ModelForm):
    class Meta:
        model = Professional
        exclude = [
            "created_at",
            "updated_at",
            "segments",
            "primary_key_words",
            "secondary_key_words",
            "sub_missions",
        ]
        widgets = {
            "activity": ActivityRadioSelect(),
            "key_words": forms.widgets.CheckboxSelectMultiple(),
        }

    activity_first = FullModelChoiceField(
        queryset=Activity.objects,
        required=True,
        to_field_name="pk",
    )
    activity_second = FullModelChoiceField(
        queryset=Activity.objects,
        required=False,
        to_field_name="pk",
    )
    activity_third = FullModelChoiceField(
        queryset=Activity.objects,
        required=False,
        to_field_name="pk",
    )
    activity_fourth = FullModelChoiceField(
        queryset=Activity.objects,
        required=False,
        to_field_name="pk",
    )
    job = FullModelChoiceField(
        queryset=Job.objects,
        required=True,
        to_field_name="pk",
    )
    user = FullModelChoiceField(
        queryset=User.objects,
        required=True,
        to_field_name="pk",
    )

    def save(self, commit=True):

        professional = super(ProfessionalForm, self).save(commit=False)
        if commit:
            professional.save()

        return professional

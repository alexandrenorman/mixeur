# -*- coding: utf-8 -*-
import datetime

from django import forms
from django.core.exceptions import ValidationError

import pytz

from accounts.models import User

from dialogwatt.fields.client_or_contact_field import ClientOrContactField
from dialogwatt.models import Appointment, Place, Slot

from fac.models import Contact

from helpers.forms import ISODateTimeField


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = (
            # "created_at",
            # "updated_at",
            "subject",
            "start_date",
            "end_date",
            "advisor",
            "client_or_contact",
            "place",
            "slot",
            "reason",
            "description",
            "has_been_honored",
            "group",
        )

    description = forms.CharField(required=False)
    has_been_honored = forms.BooleanField(required=False)

    advisor = forms.ModelChoiceField(
        queryset=User.advisors.filter(is_active=True),
        required=False,
        to_field_name="pk",
    )
    slot = forms.ModelChoiceField(
        queryset=Slot.selectable.all(), required=False, to_field_name="pk"
    )
    place = forms.ModelChoiceField(
        queryset=Place.objects.all(), required=False, to_field_name="pk"
    )

    client_or_contact = ClientOrContactField(required=False)
    group = forms.IntegerField(required=True)
    start_date = ISODateTimeField(required=True)
    end_date = ISODateTimeField(required=True)

    def clean(self):
        super().clean()
        client_or_contact = self.cleaned_data.get("client_or_contact")
        group = self.cleaned_data.get("group")
        if type(client_or_contact) is Contact:
            if group != client_or_contact.owning_group.pk:
                raise ValidationError("Le contact n'appartient pas à ce groupe")

        if "group" in self.cleaned_data:
            self.cleaned_data.pop("group")

        if (
            self.cleaned_data.get("slot")
            and self.cleaned_data.get("start_date")
            .astimezone(pytz.timezone("Europe/Paris"))
            .date()
            != self.cleaned_data.get("slot")
            .start_date.astimezone(pytz.timezone("Europe/Paris"))
            .date()
        ):
            slot_date = (
                self.cleaned_data.get("slot")
                .start_date.astimezone(pytz.timezone("Europe/Paris"))
                .date()
                .strftime("%d/%m/%y")
            )
            appointment_date = (
                self.cleaned_data.get("start_date")
                .astimezone(pytz.timezone("Europe/Paris"))
                .date()
                .strftime("%d/%m/%y")
            )
            raise ValidationError(
                f"Le rendez-vous est lié à un créneau du {slot_date} et ne peut pas être déplacé au {appointment_date}"
            )

        if (
            self.cleaned_data.get("end_date") - self.cleaned_data.get("start_date")
        ) < datetime.timedelta(minutes=15):
            raise ValidationError(
                "La durée minimale d'un rendez-vous est de 15 minutes"
            )

        return self.cleaned_data

    def save(self, commit=True):
        appointment = super().save(commit=commit)
        appointment.client_or_contact = self.cleaned_data["client_or_contact"]
        appointment.save()
        return appointment

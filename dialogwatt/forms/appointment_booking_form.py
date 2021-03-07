# -*- coding: utf-8 -*-
from django import forms

import pytz

from accounts.models import User

from dialogwatt.fields.client_or_contact_field import ClientOrContactField
from dialogwatt.models import Appointment

from fac.models import Contact

from helpers.forms import ISODateTimeField


class AppointmentBookingForm(forms.ModelForm):
    class Meta:
        model = Appointment
        exclude = [
            "subject",
            "sequence",
            "place",
            "created_at",
            "updated_at",
            "start_date",
            "end_date",
            "history",
        ]

    advisor = forms.ModelChoiceField(queryset=User.advisors.all(), required=False)
    client_or_contact = ClientOrContactField(required=False)
    client = forms.ModelChoiceField(queryset=User.clients.all(), required=False)
    contact = forms.ModelChoiceField(queryset=Contact.objects.all(), required=False)
    # TODO check si y a soit un client soit un contact qui appartient à la structure

    tmp_book_date = ISODateTimeField(required=False)
    time = forms.TimeField(required=True)
    status = forms.ChoiceField(choices=Appointment.STATUS, required=False)

    def _time_to_minutes(self, time) -> int:
        """
        convert Datetime.time to minutes
        """
        return time.hour * 60 + time.minute

    def clean(self):
        cleaned_data = super().clean()
        client_or_contact = cleaned_data.get("client_or_contact")
        client = cleaned_data.get("client")
        contact = cleaned_data.get("contact")
        time = cleaned_data.get("time")
        duration = cleaned_data.get("reason").duration
        slot = cleaned_data.get("slot")
        status = cleaned_data.get("status")

        if client_or_contact is None and client is not None:
            self.data["client_or_contact"] = client
            client_or_contact = client

        if client_or_contact is None and contact is not None:
            self.data["client_or_contact"] = contact
            client_or_contact = contact

        if not client_or_contact and status != "waiting":
            raise forms.ValidationError(
                "Vous devez sélectionner un client ou un contact",
                code="client_or_contact",
            )

        end_time = self._time_to_minutes(time) + duration

        # See django/dialogwatt/helpers/find_slots.py, same timezone
        tz = pytz.timezone("Europe/Paris")

        if time < slot.start_date.astimezone(tz).replace(
            microsecond=0
        ).time() or end_time > self._time_to_minutes(
            slot.end_date.astimezone(tz).time()
        ):
            raise forms.ValidationError("L'horaire est hors du créneau", code="time")

        # TODO Check that slot is still available
        return cleaned_data


class AppointmentBookingForAdvisorForm(AppointmentBookingForm):
    contact = forms.ModelChoiceField(queryset=Contact.objects.all(), required=False)

    def clean(self):
        cleaned_data = super().clean()
        client = cleaned_data.get("client")
        contact = cleaned_data.get("contact")

        if client and contact:
            raise forms.ValidationError(
                "Vous ne pouvez pas sélectionner un client et un contact",
                code="client_or_contact",
            )

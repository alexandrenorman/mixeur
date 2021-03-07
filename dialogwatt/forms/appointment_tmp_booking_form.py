# -*- coding: utf-8 -*-
from django import forms

from dialogwatt.models import Appointment

from accounts.models import User

import pytz


class AppointmentTmpBookingForm(forms.ModelForm):
    class Meta:
        model = Appointment
        exclude = [
            "status",
            "subject",
            "sequence",
            "place",
            "created_at",
            "updated_at",
            "start_date",
            "end_date",
            "history",
            "tmp_book_date",
        ]

    advisor = forms.ModelChoiceField(queryset=User.advisors.all(), required=False)
    # client_or_contact = ClientOrContactField(required=False)

    # client = forms.ModelChoiceField(queryset=User.clients.all(), required=False)
    # contact = forms.ModelChoiceField(queryset=Contact.objects.all(), required=False)
    # TODO check si y a soit un client soit un contact qui appartient à la structure

    # tmp_book_date = ISODateTimeField(required=False)
    time = forms.TimeField(required=True)
    status = forms.ChoiceField(choices=Appointment.STATUS, required=False)

    def _time_to_minutes(self, time) -> int:
        """
        convert Datetime.time to minutes
        """
        return time.hour * 60 + time.minute

    def clean(self):
        cleaned_data = super().clean()
        # client_or_contact = cleaned_data.get("client_or_contact")
        time = cleaned_data.get("time")
        duration = cleaned_data.get("reason").duration
        slot = cleaned_data.get("slot")
        # status = cleaned_data.get("status")
        #
        # if not client_or_contact and status != "waiting":
        #     raise forms.ValidationError(
        #         "Vous devez sélectionner un client ou un contact",
        #         code="client_or_contact",
        #     )

        end_time = self._time_to_minutes(time) + duration

        # See django/dialogwatt/helpers/find_slots.py, same timezone
        tz = pytz.timezone("Europe/Paris")

        if time < slot.start_date.astimezone(tz).replace(
            microsecond=0
        ).time() or end_time > self._time_to_minutes(
            slot.end_date.astimezone(tz).time()
        ):
            raise forms.ValidationError("L'horaire est hors du créneau", code="time")

        return cleaned_data
        # Check that slot is still available

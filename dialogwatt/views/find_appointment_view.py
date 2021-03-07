# -*- coding: utf-8 -*-
import json
from datetime import datetime, timedelta

from dateutil.rrule import DAILY, rrule

from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse

from rest_framework import status

from dialogwatt.forms import FindAppointmentForm
from dialogwatt.helpers.find_slots import FindSlots
from dialogwatt.models import Slot

from helpers.views import ApiView, ModelReadOnlyView


class FindAppointmentView(ModelReadOnlyView, ApiView):
    """
    | `reason`     | `Reason` - motif du rdv                    |
    | `inseecode`  | `inseeCode` - adresse du demandeur         |
    | `place`      | `place` - lieu du créneau         |
    | `startDate`  | date de début de la requête                |
    | `group`      | *optionnel* - une structure en particulier |
    | `advisor`    | *optionnel* - un conseiller en particulier |
    """

    def _fill_form(self, request):
        return FindAppointmentForm(
            {
                "reason": request.GET.get("reason", None),
                "inseecode": request.GET.get("inseecode", None),
                "start_date": request.GET.get("startDate", None),
                "advisor": request.GET.get("advisor", None),
                "place": request.GET.get("place", None),
            }
        )

    def _fill_available_slots_with_free_time(self, chunks):
        for i in chunks:
            key = json.dumps(i, cls=DjangoJSONEncoder)
            for item in chunks[i]:
                data = {
                    "time": item["time"],
                    "slot": item["slot"],
                }
                try:
                    self.available_slots[key].append(data)
                except KeyError:
                    self.available_slots[key] = [data]

    def _fill_available_slots_without_appointments(self, chunks):
        for i in chunks:
            key = json.dumps(i, cls=DjangoJSONEncoder)
            for item in chunks[i]:
                data = {
                    "start": item["start"],
                    "end": item["end"],
                    "slot": item["slot"],
                }
                try:
                    self.available_slots[key].append(data)
                except KeyError:
                    self.available_slots[key] = [data]

    def get(self, request, *args, **kwargs):
        """"""
        form = self._fill_form(request)
        if form.is_valid():
            reason = form.cleaned_data["reason"]
            if form.cleaned_data["inseecode"]:
                inseecode = form.cleaned_data["inseecode"].inseecode
            else:
                inseecode = None
            start_date = form.cleaned_data["start_date"]
            advisor = form.cleaned_data["advisor"]
            place = form.cleaned_data["place"]

            if not start_date:
                start_date = datetime.today().date()

            advisor_visibility = not (
                request.user.is_anonymous or request.user.is_client
            )
            fs = FindSlots(
                inseecode=inseecode,
                start_date=start_date,
                reason=reason,
                place=place,
                advisor_visibility=advisor_visibility,
            )

            advisor_filter = [advisor] if advisor else None

            self.available_slots = {}

            chunks = fs.find_free_time(
                duration=reason.duration, filter_advisors=advisor_filter
            )
            self._fill_available_slots_with_free_time(chunks)

            chunks = fs.find_slots_without_appointment(
                duration=reason.duration, filter_advisors=advisor_filter
            )
            self._fill_available_slots_without_appointments(chunks)

            if not self.available_slots:
                return JsonResponse({})

            for key in self.available_slots:
                self.available_slots[key].sort(key=self._get_minutes)

            last_slot_id = self.available_slots[list(self.available_slots.keys())[-1]][
                -1
            ]["slot"]
            last_date = Slot.objects.get(id=last_slot_id).end_date + timedelta(days=1)

            available_slots_including_all_days = {}
            for day in list(rrule(DAILY, until=last_date, dtstart=start_date)):
                key = f'"{day.date().isoformat()}"'
                try:
                    available_slots_including_all_days[key] = self.available_slots[key]
                except KeyError:
                    available_slots_including_all_days[key] = []

            return JsonResponse(available_slots_including_all_days)

        return JsonResponse(form.errors, status=status.HTTP_400_BAD_REQUEST)

    def _get_minutes(self, obj):
        if "start" in obj:
            key = "start"

        if "time" in obj:
            key = "time"

        h, m = [int(x) for x in obj[key].split(":")]
        return h * 60 + m

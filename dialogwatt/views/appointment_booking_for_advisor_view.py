# -*- coding: utf-8 -*-
import json

from dateutil.relativedelta import relativedelta

from django.http import JsonResponse

import pytz

from rest_framework import status

from dialogwatt.forms import AppointmentBookingForAdvisorForm
from dialogwatt.helpers import find_available_advisor_for_timeslot_in_slot
from dialogwatt.helpers.notification_manager import NotificationManager
from dialogwatt.models import Appointment
from dialogwatt.serializers import AppointmentSerializer

from helpers.views import ApiView, ModelReadOnlyView, PreventListViewMixin


class AppointmentBookingForAdvisorView(
    ModelReadOnlyView, PreventListViewMixin, ApiView
):
    """"""

    def post(self, request, *args, **kwargs):
        """"""
        object_data = json.loads(request.body)
        form = AppointmentBookingForAdvisorForm(object_data)
        if form.is_valid():
            advisor = form.cleaned_data["advisor"]
            client = form.cleaned_data["client"]
            contact = form.cleaned_data["contact"]
            reason = form.cleaned_data["reason"]
            slot = form.cleaned_data["slot"]
            time = form.cleaned_data["time"]
            description = form.cleaned_data["description"]

            start_date = (
                slot.start_date.astimezone(pytz.timezone("Europe/Paris"))
                + relativedelta(hour=time.hour)
                + relativedelta(minute=time.minute)
            )
            end_date = start_date + relativedelta(minutes=reason.duration)

            if advisor is None and slot.use_advisor_calendar:
                try:
                    advisor = find_available_advisor_for_timeslot_in_slot(
                        slot=slot, start_date=start_date, end_date=end_date
                    )
                except ValueError as e:
                    return JsonResponse(
                        {"Error": str(e)},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

            appointment = Appointment.objects.create(
                subject="RDV pris par un conseiller",
                start_date=start_date,
                end_date=end_date,
                advisor=advisor,
                client_or_contact=client or contact,
                place=slot.place,
                slot=slot,
                reason=reason,
                description=f"Rdv pris par {request.user.full_name} / {request.user.group.name}<br>{description}",
            )

            if appointment.group == self.request.user.group:
                trigger_type = "created_advisor"
            else:
                trigger_type = "created_client"

            notification_manager = NotificationManager()
            notification_manager.manage_notifications_for_object(
                origin_of_notification=appointment,
                trigger_type=trigger_type,
                group=appointment.group,
            )

            serializer = AppointmentSerializer(appointment)
            return JsonResponse(serializer.data)

        return JsonResponse(form.errors, status=status.HTTP_400_BAD_REQUEST)

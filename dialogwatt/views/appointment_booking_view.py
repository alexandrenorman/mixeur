# -*- coding: utf-8 -*-

import json

from dateutil.relativedelta import relativedelta

from django.http import JsonResponse

import pytz

from rest_framework import status

from dialogwatt.forms import AppointmentBookingForm
from dialogwatt.helpers import find_available_advisor_for_timeslot_in_slot
from dialogwatt.helpers.notification_manager import NotificationManager
from dialogwatt.models import Appointment
from dialogwatt.serializers import AppointmentSerializer

from helpers.views import ApiView, ModelReadOnlyView, PreventListViewMixin


class AppointmentBookingView(ModelReadOnlyView, PreventListViewMixin, ApiView):
    """
    Book an appointment
    """

    def post(self, request, *args, **kwargs):
        """"""
        object_data = json.loads(request.body)
        form = AppointmentBookingForm(object_data)
        if form.is_valid():
            advisor = form.cleaned_data["advisor"]
            client = form.cleaned_data["client"]
            reason = form.cleaned_data["reason"]
            slot = form.cleaned_data["slot"]
            description = form.cleaned_data["description"]
            time = form.cleaned_data["time"]
            tmp_book_date = form.cleaned_data["tmp_book_date"]
            form_answers = form.cleaned_data["form_answers"]
            if "status" in form.cleaned_data:
                appointment_status = form.cleaned_data["status"]
            else:
                appointment_status = None

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
                subject="RDV pris en ligne",
                start_date=start_date,
                end_date=end_date,
                advisor=advisor,
                client_or_contact=client,
                place=slot.place,
                slot=slot,
                tmp_book_date=tmp_book_date,
                reason=reason,
                description=description,
                status=appointment_status,
                form_answers=form_answers,
            )

            try:
                NotificationManager().manage_notifications_for_object(
                    origin_of_notification=appointment,
                    trigger_type="created_client",
                    group=appointment.group,
                )
            except ValueError:
                print("No notification for appointment.")
                pass

            serializer = AppointmentSerializer(appointment)
            return JsonResponse(serializer.data)

        return JsonResponse(form.errors, status=status.HTTP_400_BAD_REQUEST)

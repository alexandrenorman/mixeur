# -*- coding: utf-8 -*-
import json
import pytz
from datetime import datetime
from dateutil.relativedelta import relativedelta


from helpers.views import (
    ApiView,
    ModelView,
    PreventDeleteViewMixin,
    PreventListViewMixin,
)

from django.http import JsonResponse

from rest_framework import status

# from dialogwatt.helpers.find_slots import FindSlots
from dialogwatt.models import Appointment
from dialogwatt.serializers import AppointmentSerializer

from dialogwatt.forms import AppointmentForm, AppointmentTmpBookingForm
from dialogwatt.helpers import find_available_advisor_for_timeslot_in_slot
from dialogwatt.helpers.notification_manager import NotificationManager


class AppointmentTmpBookingView(
    PreventListViewMixin, PreventDeleteViewMixin, ModelView, ApiView
):
    """
    Book an appointment in WAITING status for one hour
    """

    model = Appointment
    form = AppointmentForm
    serializer = AppointmentSerializer
    perm_module = "dialogwatt/appointment"

    def post(self, request, *args, **kwargs):
        """
        """
        object_data = json.loads(request.body)
        form = AppointmentTmpBookingForm(object_data)
        if form.is_valid():
            advisor = form.cleaned_data["advisor"]
            reason = form.cleaned_data["reason"]
            slot = form.cleaned_data["slot"]
            description = form.cleaned_data["description"]
            time = form.cleaned_data["time"]
            form_answers = form.cleaned_data["form_answers"]

            tmp_book_date = datetime.now().astimezone(pytz.timezone("Europe/Paris"))

            appointment_status = Appointment.WAITING

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
                        {"Error": str(e)}, status=status.HTTP_400_BAD_REQUEST,
                    )

            appointment = Appointment.objects.create(
                subject="RDV pris en ligne",
                start_date=start_date,
                end_date=end_date,
                advisor=advisor,
                client_or_contact=None,
                place=slot.place,
                slot=slot,
                tmp_book_date=tmp_book_date,
                reason=reason,
                description=description,
                status=appointment_status,
                form_answers=form_answers,
            )

            serializer = AppointmentSerializer(appointment)
            return JsonResponse(serializer.data)

        return JsonResponse(form.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, *args, **kwargs):
        """
        Update model by [pk] and [uuid] used to confirm WAITING appointments

        Use model.change_waiting permission
        """
        try:
            pk = kwargs["pk"]
            uuid = kwargs["uuid"]
        except KeyError:
            return JsonResponse(
                {"Error": "Not Found"}, status=status.HTTP_404_NOT_FOUND
            )

        try:
            obj = Appointment.active.get(pk=pk, uuid=uuid)
        except Exception:
            return JsonResponse(
                {
                    "Error": "Not Found",
                    "message": "La réservation temporaire du rendez-vous est expirée.",
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        if not request.user.has_perm("dialogwatt/appointment.change_waiting", obj):
            return JsonResponse(
                {"error": "change not permitted"}, status=status.HTTP_403_FORBIDDEN
            )

        # Assign status and client
        # to pending appointment
        obj.status = Appointment.VALIDATED
        obj.client_or_contact = request.user
        obj.save()

        # Creation
        notification_manager = NotificationManager()
        notification_manager.manage_notifications_for_object(
            origin_of_notification=obj, trigger_type="created_client", group=obj.group,
        )

        # Notify date of appointment
        notification_manager = NotificationManager()
        notification_manager.manage_notifications_for_object(
            origin_of_notification=obj,
            trigger_type="date_of_appointment",
            group=obj.group,
        )

        return self.get(request, pk=obj.pk)

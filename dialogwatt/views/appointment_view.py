# -*- coding: utf-8 -*-
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from rest_framework import status

from dialogwatt.forms import AppointmentForm
from dialogwatt.helpers.notification_manager import NotificationManager
from dialogwatt.models import Appointment
from dialogwatt.serializers import (
    AppointmentBookInfoSerializer,
    AppointmentForSchedulerSerializer,
)

from fac.models import Contact

from helpers.mixins.mixins_recordable import RecordableViewMixin
from helpers.views import ApiView, ModelView


class AppointmentView(RecordableViewMixin, ModelView, ApiView):
    """
    AppointmentView requires authenticated user

    get :model:`dialogwatt.Appointment`

    """

    model = Appointment
    form = AppointmentForm
    serializer = AppointmentForSchedulerSerializer
    perm_module = "dialogwatt/appointment"

    def get_serializer(self, request, call):
        """
        Return serializer
        """
        if "detailed" in request.GET:
            return AppointmentBookInfoSerializer

        return self.serializer

    def filter(self, request, queryset):  # NOQA: A003
        # Only Active Appointment !
        queryset = Appointment.active.all()

        if "from" in request.GET:
            queryset = queryset.filter(start_date__gte=request.GET["from"])
        if "to" in request.GET:
            queryset = queryset.filter(end_date__lt=request.GET["to"])

        if "contact" in request.GET:
            try:
                contact = Contact.objects.get(pk=request.GET["contact"])
            except Contact.DoesNotExist:
                queryset = queryset.filter(pk=-1)
            else:
                appointments_from_client = []
                appointments = [x.pk for x in contact.appointments.all()]
                if contact.client_account:
                    appointments_from_client = [
                        x.pk for x in contact.client_account.appointments.all()
                    ]

                queryset = queryset.filter(
                    pk__in=appointments + appointments_from_client
                )

        return queryset

    def delete(self, request, *args, **kwargs):
        """
        Do not delete model but set status to "cancelled"
        """
        try:
            key = kwargs["pk"]
        except KeyError:
            return JsonResponse(
                {"Error": "Not Found"}, status=status.HTTP_404_NOT_FOUND
            )

        pk = key
        obj = get_object_or_404(self.model, pk=pk)

        perm = self.get_perm_module(request, "DELETE")
        if perm:
            if not request.user.has_perm(f"{perm}.delete", obj):
                return JsonResponse(
                    {"error": "delete not permitted"}, status=status.HTTP_403_FORBIDDEN
                )

        with transaction.atomic():
            obj.status = "cancelled"
            obj.save()

        if self.request.user.is_advisor:
            trigger_type = "cancelled_advisor"
        else:
            trigger_type = "cancelled_client"

        notification_manager = NotificationManager()
        notification_manager.manage_notifications_for_object(
            origin_of_notification=obj,
            trigger_type=trigger_type,
            group=obj.group,
        )

        return JsonResponse({"ok": "Deleted"})

    def post_save(self, request, instance, instance_data, created):
        """
        Handle call to NotificationManager as post_save action
        """
        super().post_save(request, instance, instance_data, created)

        if created:
            if instance.group == self.request.user.group:
                trigger_type = "created_advisor"
            else:
                trigger_type = "created_client"

        else:
            if instance.group == self.request.user.group:
                trigger_type = "changed_advisor"
            else:
                trigger_type = "changed_client"

        # Change or creation
        notification_manager = NotificationManager()
        notification_manager.manage_notifications_for_object(
            origin_of_notification=instance,
            trigger_type=trigger_type,
            group=instance.group,
        )

        # Notify date of appointment is now done in tasks.background_postponed_notifications

        return

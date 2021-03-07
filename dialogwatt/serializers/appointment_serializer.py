# -*- coding: utf-8 -*-
import pytz

from accounts.models import User
from accounts.serializers import GroupSimpleSerializer, UserSimpleSerializer

from dialogwatt.models import Appointment, FacContactForDialogwatt

from fac.models import Contact
from fac.serializers import ContactSerializer

from helpers.serializers import AutoModelSerializer

from .place_serializer import PlaceSerializer
from .reason_serializer import ReasonSerializer
from .slot_serializer import SlotInformationsSerializer


class AppointmentSerializer(AutoModelSerializer):
    model = Appointment
    exclude = [
        "content_type",
        "object_id",
        "calendarpermanenturl",
        "calendarpermanenturl_set",
        "contact",
        "user",
    ]

    def get_advisor(self, obj):
        advisor = obj.advisor
        if advisor is None:
            return None

        return advisor.pk

    def get_client_or_contact(self, obj):
        client_or_contact = obj.client_or_contact

        if (
            type(client_or_contact) is Contact
            or type(client_or_contact) is FacContactForDialogwatt
        ):
            serializer = ContactSerializer(client_or_contact)
            return serializer.data
        if type(client_or_contact) is User:
            serializer = UserSimpleSerializer(client_or_contact)
            return serializer.data
        return None

    def get_group(self, obj):
        group = obj.group
        if group is None:
            return None

        serializer = GroupSimpleSerializer(group)
        return serializer.data

    def get_place(self, obj):
        place = obj.place
        if place is None:
            return None

        return place.pk

    def get_slot(self, obj):
        slot = obj.slot
        if slot is None:
            return None

        return slot.pk

    def get_reason(self, obj):
        reason = obj.reason
        if reason is None:
            return None

        return reason.pk


class AppointmentBookInfoSerializer(AutoModelSerializer):
    model = Appointment
    exclude = [
        "content_type",
        "object_id",
        "client_or_contact",
        "calendarpermanenturl_set",
        "contact",
        "user",
    ]

    def get_advisor(self, obj):
        advisor = obj.advisor
        if advisor is None:
            return None

        serializer = UserSimpleSerializer(advisor)
        return serializer.data

    def get_place(self, obj):
        place = obj.place
        if place is None:
            return None

        serializer = PlaceSerializer(place)
        return serializer.data

    def get_slot(self, obj):
        slot = obj.slot
        if slot is None:
            return None

        serializer = SlotInformationsSerializer(slot)
        return serializer.data

    def get_reason(self, obj):
        reason = obj.reason
        if reason is None:
            return None

        serializer = ReasonSerializer(reason)
        return serializer.data


class AppointmentForSchedulerSerializer(AppointmentSerializer):
    model = Appointment
    exclude = [
        "content_type",
        "object_id",
        "contact",
        "user",
    ]

    def _date_in_scheduler_format(self, date):
        return date.astimezone(pytz.timezone("Europe/Paris")).strftime("%d-%m-%Y %H:%M")

    def get_start_date(self, obj):
        return obj.start_date

    def get_end_date(self, obj):
        return obj.end_date

    def get_real_start_date(self, obj):
        return obj.start_date

    def get_real_end_date(self, obj):
        return obj.end_date

    def get_color(self, obj):
        if obj.advisor:
            return obj.advisor.color

        return None

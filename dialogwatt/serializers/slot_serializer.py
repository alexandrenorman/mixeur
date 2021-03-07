# -*- coding: utf-8 -*-

import pytz
import serpy

from helpers.serializers import ModelSerializer
from accounts.serializers import (
    UserSimpleSerializer,
    GroupSimpleWithoutAdminGroupSerializer,
)
from .place_serializer import PlaceSerializer, PlaceSimpleSerializer
from .catchment_area_serializer import CatchmentAreaSimpleSerializer


class SlotSerializer(ModelSerializer):
    text = serpy.Field()
    group = serpy.MethodField()
    place = PlaceSimpleSerializer
    catchment_area = CatchmentAreaSimpleSerializer()
    start_date = serpy.Field()
    end_date = serpy.Field()
    visibility = serpy.Field()
    deadline = serpy.Field()
    time_between_slots = serpy.Field()
    use_advisor_calendar = serpy.Field()
    number_of_active_advisors = serpy.Field()
    advisors = serpy.MethodField()
    description = serpy.Field()
    status = serpy.Field()
    public_description = serpy.Field()
    has_appointments = serpy.MethodField()
    uuid = serpy.Field()

    def get_has_appointments(self, obj):
        return obj.has_appointments

    def get_advisors(self, obj):
        advisors = obj.advisors.all()
        serializer = UserSimpleSerializer(advisors, many=True)
        return serializer.data

    def get_group(self, obj):
        return obj.group.pk


class SlotForSchedulerSerializer(ModelSerializer):
    id = serpy.MethodField()
    text = serpy.Field()
    group = serpy.MethodField()
    place = serpy.MethodField()
    catchment_area = serpy.MethodField()
    start_date = serpy.MethodField()
    end_date = serpy.MethodField()
    real_start_date = serpy.MethodField()
    real_end_date = serpy.MethodField()
    visibility = serpy.Field()
    deadline = serpy.Field()
    time_between_slots = serpy.Field()
    use_advisor_calendar = serpy.Field()
    number_of_active_advisors = serpy.Field()
    advisors = serpy.MethodField()
    description = serpy.Field()
    public_description = serpy.Field()
    color = serpy.MethodField()
    text_color = serpy.MethodField()
    reasons = serpy.MethodField()
    status = serpy.Field()
    has_appointments = serpy.MethodField()
    uuid = serpy.Field()

    def get_has_appointments(self, obj):
        return obj.has_appointments

    def get_id(self, obj):
        return obj.pk

    def get_advisors(self, obj):
        return [
            x["user_id"]
            for x in obj.advisors.through.objects.filter(slot_id=obj.pk).values(
                "user_id"
            )
        ]
        # advisors = obj.advisors.all()
        # serializer = UserSimpleSerializer(advisors, many=True)
        # return serializer.data

    def get_group(self, obj):
        return obj.group.pk

    def get_place(self, obj):
        return obj.place.pk

    def get_reasons(self, obj):
        return [
            x["reason_id"]
            for x in obj.reasons.through.objects.filter(slot_id=obj.pk).values(
                "reason_id"
            )
        ]
        # reasons = obj.reasons.all()
        # serializer = ReasonSimpleSerializer(reasons, many=True)
        # return serializer.data

    def get_catchment_area(self, obj):
        return obj.catchment_area.pk

    def _date_in_scheduler_format(self, date):
        return date.astimezone(pytz.timezone("Europe/Paris")).strftime("%d-%m-%Y %H:%M")

    def get_start_date(self, obj):
        return obj.start_date
        # return self._date_in_scheduler_format(obj.start_date)

    def get_end_date(self, obj):
        return obj.end_date
        # return self._date_in_scheduler_format(obj.end_date)

    def get_real_start_date(self, obj):
        return obj.start_date

    def get_real_end_date(self, obj):
        return obj.end_date

    def get_color(self, obj):
        return obj.place.color

    def get_text_color(self, obj):
        return "#333"

    # return obj.end_date.strftime("%d-%m-%Y %H:%M")


class SlotInformationsSerializer(ModelSerializer):
    text = serpy.Field()
    group = GroupSimpleWithoutAdminGroupSerializer()
    place = PlaceSerializer()
    start_date = serpy.Field()
    end_date = serpy.Field()
    visibility = serpy.Field()
    deadline = serpy.Field()
    # time_between_slots = serpy.Field()
    use_advisor_calendar = serpy.Field()
    number_of_active_advisors = serpy.Field()
    advisors = serpy.MethodField()
    status = serpy.Field()
    description = serpy.Field()
    public_description = serpy.Field()
    uuid = serpy.Field()

    def get_advisors(self, obj):
        advisors = obj.advisors.all()
        serializer = UserSimpleSerializer(advisors, many=True)
        return serializer.data

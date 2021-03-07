# -*- coding: utf-8 -*-

from helpers.serializers import AutoModelSerializer
from dialogwatt.models import CalendarPermanentUrl

from accounts.serializers import UserSimpleSerializer
from dialogwatt.serializers import PlaceSimpleSerializer
from dialogwatt.serializers import ReasonSimpleSerializer


class CalendarPermanentUrlSerializer(AutoModelSerializer):
    model = CalendarPermanentUrl
    exclude = ["calendarpermanenturl"]

    def get_user(self, obj):
        serializer = UserSimpleSerializer(obj.user)
        return serializer.data

    def get_advisors(self, obj):
        serializer = UserSimpleSerializer(obj.advisors.all(), many=True)
        return serializer.data

    def get_places(self, obj):
        serializer = PlaceSimpleSerializer(obj.places.all(), many=True)
        return serializer.data

    def get_reasons(self, obj):
        serializer = ReasonSimpleSerializer(obj.reasons.all(), many=True)
        return serializer.data

# -*- coding: utf-8 -*-

from helpers.serializers import AutoModelSerializer

from dialogwatt.models import Notification


class NotificationSerializer(AutoModelSerializer):
    model = Notification

    def get_group(self, obj):
        return obj.group.pk

    def get_advisors(self, obj):
        advisors = obj.advisors.all()
        return self._get_pk(advisors)

    def get_places(self, obj):
        places = obj.places.all()
        return self._get_pk(places)

    def get_reasons(self, obj):
        reasons = obj.reasons.all()
        return self._get_pk(reasons)

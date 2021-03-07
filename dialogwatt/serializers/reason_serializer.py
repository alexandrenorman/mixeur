# -*- coding: utf-8 -*-
import html2text

from helpers.serializers import AutoModelSerializer
from dialogwatt.models import Reason
from accounts.models import User
from accounts.serializers import UserSimpleSerializer


class ReasonSerializer(AutoModelSerializer):
    model = Reason
    exclude = [
        "slot",
        "notification",
        "appointment",
        "calendarpermanenturl",
        "calendarpermanenturl_set",
    ]

    def get_group(self, obj):
        return obj.group.pk

    def get_description_as_text(self, obj):
        if obj.show_description and obj.description:
            return html2text.html2text(obj.description).replace("\n", " ")

        return ""


class ReasonSimpleSerializer(AutoModelSerializer):
    model = Reason
    exclude = [
        "slot",
        "form",
        "notification",
        "appointment",
        "calendarpermanenturl",
        "calendarpermanenturl_set",
    ]

    def get_group(self, obj):
        return obj.group.pk


class FindReasonsSerializer(AutoModelSerializer):
    model = Reason
    exclude = [
        "slot",
        "notification",
        "appointment",
        "calendarpermanenturl",
        "calendarpermanenturl_set",
    ]

    def get_group(self, obj):
        return obj.group.pk

    def get_advisors(self, obj):
        advisors = User.objects.filter(
            is_active=True, slot__in=obj.slot_set.all()
        ).distinct()

        advisors = sorted(advisors, key=lambda x: x.full_name)
        return UserSimpleSerializer(advisors, many=True).data

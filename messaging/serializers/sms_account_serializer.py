# -*- coding: utf-8 -*-
from helpers.serializers import AutoModelSerializer
from messaging.models import SmsAccount


class SmsAccountSerializer(AutoModelSerializer):
    model = SmsAccount

    def get_group(self, obj):
        """
        get field group of type OneToOneField
        """
        return obj.group.pk

    def get_phone(self, obj):
        """
        get field phone of type PhoneNumberField
        """
        if obj.phone:
            return f"{obj.phone}"
        else:
            return ""

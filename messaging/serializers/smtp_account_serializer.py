# -*- coding: utf-8 -*-
from helpers.serializers import AutoModelSerializer
from messaging.models import SmtpAccount


class SmtpAccountSerializer(AutoModelSerializer):
    model = SmtpAccount

    def get_group(self, obj):
        """
        get field group of type OneToOneField
        """
        return obj.group.pk

# -*- coding: utf-8 -*-

from helpers.serializers import AutoModelSerializer

from dialogwatt.models import Exchange


class ExchangeSerializer(AutoModelSerializer):
    model = Exchange
    exclude = ["attachments", "background_task", "content_type", "object_id", "group"]

    def get_from_account(self, obj):
        return (
            f"{obj.from_account.full_name} <{obj.from_account.email}>"
            if obj.from_account is not None
            else ""
        )

    def get_to_account(self, obj):
        return (
            f"{obj.to_account.full_name} <{obj.to_account.email}>"
            if obj.to_account is not None
            else ""
        )

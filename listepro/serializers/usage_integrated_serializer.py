# -*- coding: utf-8 -*-
from helpers.serializers import AutoModelSerializer

from listepro.models import UsageIntegrated


class UsageIntegratedSerializer(AutoModelSerializer):
    model = UsageIntegrated

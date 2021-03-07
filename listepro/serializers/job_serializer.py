# -*- coding: utf-8 -*-
from helpers.serializers import AutoModelSerializer

from listepro.models import Job


class JobSerializer(AutoModelSerializer):
    model = Job

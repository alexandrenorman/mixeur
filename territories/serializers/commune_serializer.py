# -*- coding: utf-8 -*-
from helpers.serializers import AutoModelSerializer
from territories.models import Commune


class CommuneSerializer(AutoModelSerializer):
    model = Commune
    exclude = ["departement", "region", "epci"]

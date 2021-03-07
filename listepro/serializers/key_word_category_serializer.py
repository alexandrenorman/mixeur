# -*- coding: utf-8 -*-
from helpers.serializers import AutoModelSerializer

from listepro.models import KeyWordCategory


class KeyWordCategorySerializer(AutoModelSerializer):
    model = KeyWordCategory

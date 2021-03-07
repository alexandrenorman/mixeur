# -*- coding: utf-8 -*-
from helpers.serializers import AutoModelSerializer

from listepro.models import ProfessionalImage


class ProfessionalImageSerializer(AutoModelSerializer):
    model = ProfessionalImage

    def get_production(self, obj):
        """
        get field get_production of type ForeignKey
        """
        return obj.production.pk

    def get_cropped(self, obj):
        if obj.cropped:
            return obj.cropped.url
        else:
            return None

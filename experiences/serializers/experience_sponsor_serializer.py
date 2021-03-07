# -*- coding: utf-8 -*-
import html2text
from helpers.serializers import AutoModelSerializer
from experiences.models import ExperienceSponsor

from .sponsor_tag_serializer import SponsorTagSerializer


class ExperienceSponsorSerializer(AutoModelSerializer):
    model = ExperienceSponsor

    def get_description_as_ascii(self, obj):
        return html2text.html2text(obj.description)

    def get_sponsor(self, obj):
        sponsor = obj.sponsor
        serializer = SponsorTagSerializer(sponsor)
        return serializer.data

    def get_owning_group(self, obj):
        """
        get field owning_group of type ForeignKey
        """
        if not obj.owning_group:
            return None

        return obj.owning_group.pk

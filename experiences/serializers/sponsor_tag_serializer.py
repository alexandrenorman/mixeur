# -*- coding: utf-8 -*-
from .abstract_tag_serializer import AbstractTagSerializer
from experiences.models import SponsorTag


class SponsorTagSerializer(AbstractTagSerializer):
    model = SponsorTag

    def get_count_experiences(self, obj):
        return obj.experiences_sponsors.count()

# -*- coding: utf-8 -*-
from experiences.models import YearTag
from .abstract_tag_serializer import AbstractTagSerializer


class YearTagSerializer(AbstractTagSerializer):
    model = YearTag

    def get_count_experiences(self, obj):
        return obj.experience_years.count()

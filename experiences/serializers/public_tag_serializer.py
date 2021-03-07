# -*- coding: utf-8 -*-
from experiences.models import PublicTag
from .abstract_tag_serializer import AbstractTagSerializer


class PublicTagSerializer(AbstractTagSerializer):
    model = PublicTag

    def get_count_experiences(self, obj):
        return obj.experience_publics.count()

# -*- coding: utf-8 -*-
from experiences.models import ExperienceTag
from .abstract_tag_serializer import AbstractTagSerializer


class ExperienceTagSerializer(AbstractTagSerializer):
    model = ExperienceTag

    def get_count_experiences(self, obj):
        return obj.experience_tags.count()

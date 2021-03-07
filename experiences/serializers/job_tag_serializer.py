# -*- coding: utf-8 -*-
from experiences.models import JobTag
from .abstract_tag_serializer import AbstractTagSerializer


class JobTagSerializer(AbstractTagSerializer):
    model = JobTag

    def get_count_experiences(self, obj):
        return obj.experience_jobs.count()

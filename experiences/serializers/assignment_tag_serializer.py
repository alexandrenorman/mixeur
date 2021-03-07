# -*- coding: utf-8 -*-
from experiences.models import AssignmentTag
from .abstract_tag_serializer import AbstractTagSerializer


class AssignmentTagSerializer(AbstractTagSerializer):
    model = AssignmentTag

    def get_count_experiences(self, obj):
        return obj.experience_assignments.count()

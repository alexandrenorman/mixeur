# -*- coding: utf-8 -*-
from experiences.models import PartnerTag
from .abstract_tag_serializer import AbstractTagSerializer


class PartnerTagSerializer(AbstractTagSerializer):
    model = PartnerTag

    # def get_name_eu(self, obj):
    #     return f"EU - {obj.name}" if obj.is_european else f"FR - {obj.name}"
    def get_count_experiences(self, obj):
        return obj.experience_partners.count()

# -*- coding: utf-8 -*-
from helpers.serializers import AutoModelSerializer
from newsletters.models import Newsletter


class NewsletterSerializer(AutoModelSerializer):
    model = Newsletter

    def get_group_of_newsletters(self, obj):
        """
        get field group_of_newsletters of type ForeignKey
        """
        return obj.group_of_newsletters.pk

    def get_is_published(self, obj):
        return obj.is_published

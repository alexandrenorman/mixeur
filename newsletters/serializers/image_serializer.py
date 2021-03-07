# -*- coding: utf-8 -*-
from helpers.serializers import AutoModelSerializer
from newsletters.models import Image


class ImageSerializer(AutoModelSerializer):
    model = Image

    # def get_newsletter(self, obj):
    #     """
    #     get field newsletter of type ForeignKey
    #     """
    #     return obj.newsletter.pk

    def get_image(self, obj):
        return obj.image.url

    def get_group(self, obj):
        return obj.group.pk

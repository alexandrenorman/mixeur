# -*- coding: utf-8 -*-
from helpers.serializers import AutoModelSerializer
from newsletters.models import GroupOfNewsletters


class GroupOfNewslettersSerializer(AutoModelSerializer):
    model = GroupOfNewsletters

    def get_group(self, obj):
        """
        get field group of type ForeignKey
        """
        return obj.group.pk

    def get_has_published_newsletters(self, obj):
        return obj.has_published_newsletters

    def get_count_newsletters(self, obj):
        """
        Count newsletters for this group
        """
        return obj.newsletter_set.count()

    def get_header(self, obj):
        if obj.header:
            return obj.header.url
        else:
            return None

    def get_footer(self, obj):
        if obj.footer:
            return obj.footer.url
        else:
            return None

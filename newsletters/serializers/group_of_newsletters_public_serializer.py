# -*- coding: utf-8 -*-
import serpy
from helpers.serializers import AutoModelSerializer
from newsletters.models import GroupOfNewsletters


class NewsletterSimpleSerializer(serpy.Serializer):
    pk = serpy.Field()
    slug = serpy.Field()
    title = serpy.Field()
    is_active = serpy.Field()
    is_public = serpy.Field()
    is_published = serpy.Field()
    publication_start_date = serpy.Field()
    description = serpy.Field()


class GroupOfNewslettersPublicSerializer(AutoModelSerializer):
    model = GroupOfNewsletters

    def get_newsletters(self, obj):
        newsletters = obj.newsletter_set.all()

        # Get only published newsletters
        published = [x.pk for x in newsletters if x.is_published]
        newsletters = newsletters.filter(pk__in=published).order_by(
            "-publication_start_date"
        )

        newsletters_serializer = NewsletterSimpleSerializer(newsletters, many=True)
        return newsletters_serializer.data

    def get_group(self, obj):
        """
        get field group of type ForeignKey
        """
        return obj.group.pk

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

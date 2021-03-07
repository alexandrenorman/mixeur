# -*- coding: utf-8 -*-
from fac.models import Tag
from helpers.serializers import AutoModelSerializer


class SimpleTagSerializer(AutoModelSerializer):
    model = Tag

    def get_owning_group(self, obj):
        """
        get field owning_group of type ForeignKey
        """
        if not obj.owning_group:
            return None

        return obj.owning_group.pk

    def get_nb_contacts(self, obj):
        """
        get the number of contacts linked to this tag
        """
        return obj.contacts.count()

    def get_nb_organizations(self, obj):
        """
        get the number of organizations linked to this tag
        """
        return obj.organizations.count()

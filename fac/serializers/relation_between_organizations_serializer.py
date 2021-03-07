# -*- coding: utf-8 -*-
import serpy
from fac.models import RelationBetweenOrganization
from helpers.serializers import AutoModelSerializer


class RelationBetweenOrganizationSerializer(AutoModelSerializer):
    model = RelationBetweenOrganization

    display_name = serpy.MethodField()

    def get_owning_group(self, obj):
        """
        get field owning_group of type ForeignKey
        """
        if not obj.owning_group:
            return None

        return obj.owning_group.pk

    def get_first_organization(self, obj):
        """
        get field first_organization of type ForeignKey
        """
        return obj.first_organization.pk

    def get_second_organization(self, obj):
        """
        get field second_organization of type ForeignKey
        """
        return obj.second_organization.pk

    def get_display_name(self, obj):
        return str(obj)

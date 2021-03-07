# -*- coding: utf-8 -*-
import serpy

from fac.serializers import ContactSerializer
from fac.serializers import OrganizationSerializer


class EntitiesListSerializer(serpy.Serializer):
    contacts = ContactSerializer(many=True, required=False)
    organizations = OrganizationSerializer(many=True, required=False)

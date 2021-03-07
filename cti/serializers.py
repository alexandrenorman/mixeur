# -*- coding: utf-8 -*-

import serpy

from accounts.serializers.user_simple_serializer import UserSimpleSerializer

from fac.serializers import ContactSerializer, OrganizationSerializer


class CtiSerializer(serpy.DictSerializer):
    users = UserSimpleSerializer(many=True)
    contacts = ContactSerializer(many=True)
    organizations = OrganizationSerializer(many=True)

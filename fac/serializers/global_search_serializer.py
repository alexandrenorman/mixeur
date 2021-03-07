# -*- coding: utf-8 -*-
import serpy

from accounts.serializers import UserSerializer
from .contact_serializer import ContactSerializer
from .tag_serializer import TagSerializer
from .organization_serializer import OrganizationSerializer


class GlobalSearchSerializer(serpy.Serializer):
    clients = UserSerializer(many=True, required=False)
    contacts = ContactSerializer(many=True, required=False)
    organizations = OrganizationSerializer(many=True, required=False)
    tags = TagSerializer(many=True, required=False)

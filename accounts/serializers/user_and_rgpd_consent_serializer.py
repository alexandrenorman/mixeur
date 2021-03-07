# -*- coding: utf-8 -*-

import serpy
from .user_serializer import UserSerializer
from .rgpd_consent_serializer import RgpdConsentSerializer


class UserAndRgpdConsentSerializer(serpy.DictSerializer):
    user = UserSerializer()
    rgpd_consent = RgpdConsentSerializer()
    domain_name = serpy.Field(required=False)

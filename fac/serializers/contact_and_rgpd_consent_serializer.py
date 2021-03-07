# -*- coding: utf-8 -*-

import serpy
from .contact_serializer import ContactSerializer
from .rgpd_consent_for_contacts_serializer import RgpdConsentForContactsSerializer


class ContactAndRgpdConsentSerializer(serpy.DictSerializer):
    contact = ContactSerializer()
    rgpd_consent = RgpdConsentForContactsSerializer()

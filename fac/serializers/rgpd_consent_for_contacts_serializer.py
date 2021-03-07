# -*- coding: utf-8 -*-

import serpy


class RgpdConsentForContactsSerializer(serpy.Serializer):
    pk = serpy.Field()
    creation_date = serpy.Field()
    allow_to_keep_data = serpy.BoolField()
    allow_to_use_phone_number_to_send_reminder = serpy.BoolField()
    allow_to_use_email_to_send_reminder = serpy.BoolField()
    allow_to_share_my_information_with_my_advisor = serpy.BoolField()
    allow_to_share_my_information_with_partners = serpy.BoolField()

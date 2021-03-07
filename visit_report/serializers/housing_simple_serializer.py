# -*- coding: utf-8 -*-
import serpy


class HousingSimpleSerializer(serpy.Serializer):
    """
    Housing serializer without user
    """

    pk = serpy.Field()
    address = serpy.Field()
    address_more = serpy.Field()
    city = serpy.Field()
    postcode = serpy.Field()
    inseecode = serpy.Field()
    housing_type = serpy.Field()
    ownership = serpy.Field()
    area = serpy.Field()
    occupants_number = serpy.Field()
    note = serpy.Field()
    is_main_address = serpy.Field()

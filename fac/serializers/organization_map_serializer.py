# -*- coding: utf-8 -*-
import serpy


class OrganizationMapSerializer(
    serpy.Serializer,
):
    pk = serpy.Field()
    name = serpy.Field()
    address = serpy.Field()
    town = serpy.Field()
    type_of_organization = serpy.Field()
    lat = serpy.Field()
    lon = serpy.Field()

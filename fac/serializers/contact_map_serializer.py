# -*- coding: utf-8 -*-
import serpy


class ContactMapSerializer(
    serpy.Serializer,
):
    pk = serpy.Field()
    full_name = serpy.Field()
    address = serpy.Field()
    lat = serpy.MethodField()
    lon = serpy.MethodField()

    def get_lat(self, obj):
        if obj.lat == 0:
            try:
                lat, lon = [
                    (x.organization.lat, x.organization.lon)
                    for x in obj.memberoforganization_set.all()
                    if x.use_address_from_organization
                ][0]
            except IndexError:
                return obj.lat

            return lat

        return obj.lat

    def get_lon(self, obj):
        if obj.lon == 0:
            try:
                lat, lon = [
                    (x.organization.lat, x.organization.lon)
                    for x in obj.memberoforganization_set.all()
                    if x.use_address_from_organization
                ][0]
            except IndexError:
                return obj.lon

            return lon

        return obj.lon

# -*- coding: utf-8 -*-
import serpy


class CommuneForGroupSerializer(serpy.Serializer):
    pk = serpy.Field()
    id = serpy.Field()
    name = serpy.Field()
    epci = serpy.MethodField()

    def get_epci(self, obj):
        return obj.epci.pk

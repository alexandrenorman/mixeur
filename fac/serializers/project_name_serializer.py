# -*- coding: utf-8 -*-

import serpy


class ProjectNameSerializer(serpy.Serializer):
    pk = serpy.Field()
    name = serpy.Field()

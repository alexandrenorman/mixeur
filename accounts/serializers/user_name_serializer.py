# -*- coding: utf-8 -*-

import serpy


class UserNameSerializer(serpy.Serializer):
    pk = serpy.Field()
    full_name = serpy.Field()

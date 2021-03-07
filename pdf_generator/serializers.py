# -*- coding: utf-8 -*-
import serpy


class PdfTempStoreSerializer(serpy.Serializer):
    uuid = serpy.Field()
    data = serpy.Field()
    created_at = serpy.Field()
    updated_at = serpy.Field()

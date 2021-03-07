# -*- coding: utf-8 -*-
import serpy


class IncompleteModelSerializer(serpy.Serializer):
    pk = serpy.Field()
    fields = serpy.Field()
    incomplete_object = serpy.MethodField()

    def get_incomplete_object(self, obj):
        if obj.incomplete_object.__class__.__name__ == "Contact":
            return {
                "class": "Contact",
                "pk": obj.incomplete_object.pk,
                "name": obj.incomplete_object.full_name,
                "first_name": obj.incomplete_object.first_name,
                "last_name": obj.incomplete_object.last_name,
            }

        if obj.incomplete_object.__class__.__name__ == "Organization":
            return {
                "class": "Organization",
                "pk": obj.incomplete_object.pk,
                "name": obj.incomplete_object.name,
            }

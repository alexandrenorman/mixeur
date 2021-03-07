from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.db.models.fields.files import FileField
from django.db.models.fields.reverse_related import (
    ForeignObjectRel,
    ManyToManyRel,
    ManyToOneRel,
    OneToOneRel,
)

import serpy

from tagulous.models.fields import TagField


"""
from dialogwatt.serializers import ReasonSerializer
a=Reason.objects.last()
b=ReasonSerializer(a)
"""


class ModelSerializer(serpy.Serializer):
    """
    Base serializer including pk, created_at and updated_at fields
    """

    pk = serpy.Field()
    created_at = serpy.Field()
    updated_at = serpy.Field()


EXCLUDED_FIELD_TYPE = (
    ManyToOneRel,
    ForeignObjectRel,
    ManyToManyRel,
    OneToOneRel,
    GenericRelation,
    FileField,
    TagField,
)

DJANGO_SERPY_FIELDS_MAPPING = {
    models.BooleanField: serpy.BoolField,
    models.DecimalField: serpy.FloatField,
    models.IntegerField: serpy.IntField,
    models.PositiveIntegerField: serpy.IntField,
    models.PositiveSmallIntegerField: serpy.IntField,
}


class AutoModelSerializer(serpy.Serializer):
    """
    Serializer for a model. It automagically include all fields from the model.
    If the serializer has a method get_field, it automatically add it as a serpy.MethodField
    otherwise it uses serpy.Field

    example:
        class ReasonSerializer(AutoModelSerializer):
            model = Reason

            def get_group(self, obj,):
                return obj.group.pk
    """

    model = None
    fields = []
    exclude = []
    include_properties = False

    def __init__(self, instance=None, many=False, data=None, context=None, **kwargs):
        self._field_map = {
            "pk": serpy.Field(),
            **self._get_model_fields(),
            **self._get_property_fields(),
            **self._get_method_fields(),
        }

        # Remove manually excluded fields
        for excluded_field_name in self.exclude:
            if excluded_field_name in self._field_map:
                del self._field_map[excluded_field_name]

        # Compile field_map for internal use
        self._compiled_fields = list(self._compiled_fields)
        for field_name in self._field_map:
            if field_name not in [x[0] for x in self._compiled_fields]:
                cmap = serpy.serializer._compile_field_to_tuple(
                    self._field_map[field_name], field_name, self
                )
                # Hack for get_field methods
                cmap = (cmap[0], cmap[1], cmap[2], cmap[3], cmap[4], False)
                self._compiled_fields.append(cmap)

        super().__init__(
            instance=instance, many=many, data=data, context=context, **kwargs
        )

    def _get_pk(self, objects):
        """
        Return a list of PK from an objects list
        """
        return [x.pk for x in objects]

    def _get_model_fields(self):
        if self.fields:
            return {
                field.name: DJANGO_SERPY_FIELDS_MAPPING.get(type(field), serpy.Field)(
                    required=False
                )
                for field in self.model._meta.get_fields()
                if type(field) not in EXCLUDED_FIELD_TYPE
                and (field.name in self.fields or len(self.fields) == 0)
            }
        else:
            return {
                field.name: DJANGO_SERPY_FIELDS_MAPPING.get(type(field), serpy.Field)(
                    required=False
                )
                for field in self.model._meta.get_fields()
                if type(field) not in EXCLUDED_FIELD_TYPE
            }

    def _get_property_fields(self):
        if not self.include_properties:
            return {}
        return {
            name: serpy.Field()
            for name in dir(self.model)
            if isinstance(getattr(self.model, name), property)
        }

    def _get_method_fields(self):
        # [4:] to skip "get_"
        return {
            method_name[4:]: serpy.MethodField()
            for method_name in dir(self)
            if method_name.startswith("get_")
        }


class PhoneSerializerMixin(serpy.Serializer):
    """
    Mixin for adding phone field on a serializer
    """

    phone = serpy.MethodField()

    def get_phone(self, obj):
        if obj.phone:
            return f"{obj.phone}"
        else:
            return ""


class MobilePhoneSerializerMixin(serpy.Serializer):
    """
    Mixin for adding mobile_phone field on a serializer
    """

    mobile_phone = serpy.MethodField()

    def get_mobile_phone(self, obj):
        if obj.mobile_phone:
            return f"{obj.mobile_phone}"
        else:
            return ""


class FaxSerializerMixin(serpy.Serializer):
    """
    Mixin for adding fax field on a serializer
    """

    fax = serpy.MethodField()

    def get_fax(self, obj):
        if obj.fax:
            return f"{obj.fax}"
        else:
            return ""


# TBD class GenericModelSerializer(AutoModelSerializer):
# TBD     """
# TBD     Create an autogenerated Model serializer at run
# TBD
# TBD     >>> s = GenericModelSerializer(Reason.objects.last(), model=Reason)
# TBD     """
# TBD     def __init__(self, instance=None, many=False, data=None, context=None, model=None, exclude=[], **kwargs):
# TBD         self._field_map = {}
# TBD         self._compiled_fields = ()
# TBD
# TBD         self.model = model
# TBD         self.exclude = []
# TBD
# TBD         return super().__init__(
# TBD             instance=instance, many=many, data=data, context=context, **kwargs
# TBD         )

# -*- coding: utf-8 -*-

import serpy

# https://django-test-plus.readthedocs.io/en/latest/
from test_plus.test import TestCase

from energies.models import Energy, EnergyVector
from helpers.serializers import AutoModelSerializer


# NOTE : We use existing true real models here because
# there is no obvious way to create a fake django model for testing


class TestAutoModelSerializer(AutoModelSerializer):
    model = EnergyVector


class TestAutoModelWithExcludedSerializer(AutoModelSerializer):
    model = Energy
    exclude = ("created_at", "updated_at", "blop")

    def get_blop(self):
        return 42


class TestAutoModelMethodOverrideSerializer(AutoModelSerializer):
    model = EnergyVector  # has pci and unit field

    def get_unit(self):
        return "yo"


class TestAutoModelMethodSerializer(AutoModelSerializer):
    model = EnergyVector

    def get_blop(self):
        return 42


class TestAutoModelWithPropertiesSerializer(AutoModelSerializer):
    model = Energy  # has name property
    include_properties = True


class TestAutoModelWithoutPropertiesSerializer(AutoModelSerializer):
    model = Energy  # has name property
    include_properties = False


class AutoModelSerializerTestCase(TestCase):
    def test_model_fields(self):
        serializer = TestAutoModelSerializer()
        self.assertEqual(
            [
                "pk",
                "id",
                "created_at",
                "updated_at",
                "vector",
                "buying_unit",
                "pci",
                "unit",
                "energy",
                "order",
            ],
            list(serializer._field_map.keys()),
        )

    def test_exclude(self):
        serializer = TestAutoModelWithExcludedSerializer()
        # reverse relations excluded
        # method get_blop excluded because in excluded fields
        excluded_fields = (
            "yearly_energy_price",
            "vectors",
            "production_systems",
            "created_at",
            "updated_at",
            "blop",
        )
        for excluded_field in excluded_fields:
            self.assertNotIn(excluded_field, serializer._field_map)

    def test_method_override(self):
        serializer = TestAutoModelMethodOverrideSerializer()
        self.assertEqual(serpy.MethodField, type(serializer._field_map["unit"]))
        self.assertEqual(serpy.FloatField, type(serializer._field_map["pci"]))

    def test_method_fetch(self):
        serializer = TestAutoModelMethodSerializer()
        self.assertEqual(serpy.MethodField, type(serializer._field_map["blop"]))

    def test_propery_fetch(self):
        serializer = TestAutoModelWithPropertiesSerializer()
        self.assertEqual(serpy.Field, type(serializer._field_map["name"]))

    def test_not_include_properties(self):
        serializer = TestAutoModelWithoutPropertiesSerializer()
        self.assertNotIn("name", serializer._field_map)

    def test_field_type_mapping(self):
        serializer = TestAutoModelWithoutPropertiesSerializer()
        self.assertEqual(serpy.IntField, type(serializer._field_map["pci_ratio"]))
        self.assertEqual(serpy.FloatField, type(serializer._field_map["ghg_ratio"]))
        self.assertEqual(serpy.BoolField, type(serializer._field_map["carbon_tax"]))

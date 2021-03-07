# https://django-test-plus.readthedocs.io/en/latest/
from decimal import Decimal

from test_plus.test import TestCase

from energies.models import ProductionSystem, SecondaryEfficiency
from energies.tests.factories import ProductionSystemFactory


class SecondaryEfficiencyTest(TestCase):
    def test_values(self):
        self.assertEqual(
            Decimal("0.85"),
            SecondaryEfficiency.get(is_heating=True, is_multi_unit=True),
        )
        self.assertEqual(
            Decimal("0.50"),
            SecondaryEfficiency.get(is_heating=False, is_multi_unit=True),
        )
        self.assertEqual(
            Decimal("0.85"),
            SecondaryEfficiency.get(
                is_heating=True, is_multi_unit=False, is_hydro=True
            ),
        )
        self.assertEqual(
            Decimal("0.87"),
            SecondaryEfficiency.get(
                is_heating=False, is_multi_unit=False, is_hydro=True
            ),
        )
        self.assertEqual(
            Decimal("1"),
            SecondaryEfficiency.get(
                is_heating=True, is_multi_unit=False, is_hydro=False
            ),
        )
        self.assertEqual(
            Decimal("1"),
            SecondaryEfficiency.get(
                is_heating=False, is_multi_unit=False, is_hydro=False
            ),
        )


class ProductionSystemTest(TestCase):
    def test_clean(self):  # NOQA: CFQ001

        # Here, we ensure that when adding fields in the model we do not have to test that new fields.
        tested_fields = {
            "id",
            "created_at",
            "updated_at",
            "identifier",
            "energy",
            "is_heating",
            "is_hot_water",
            "is_individual",
            "is_multi_unit",
            "is_hydro",
            "efficiency_heating",
            "enr_ratio_heating",
            "investment_individual_heating",
            "maintenance_individual_heating",
            "investment_small_multi_unit_heating",
            "maintenance_small_multi_unit_heating",
            "provisions_small_multi_unit_heating",
            "investment_medium_multi_unit_heating",
            "maintenance_medium_multi_unit_heating",
            "provisions_medium_multi_unit_heating",
            "investment_large_multi_unit_heating",
            "maintenance_large_multi_unit_heating",
            "provisions_large_multi_unit_heating",
            "efficiency_hot_water",
            "enr_ratio_hot_water",
            "investment_individual_hot_water",
            "maintenance_individual_hot_water",
            "investment_small_multi_unit_hot_water",
            "maintenance_small_multi_unit_hot_water",
            "provisions_small_multi_unit_hot_water",
            "investment_medium_multi_unit_hot_water",
            "maintenance_medium_multi_unit_hot_water",
            "provisions_medium_multi_unit_hot_water",
            "investment_large_multi_unit_hot_water",
            "maintenance_large_multi_unit_hot_water",
            "provisions_large_multi_unit_hot_water",
        }

        all_fields = {field.name for field in ProductionSystem._meta.get_fields()}
        missing_test_fields = all_fields - tested_fields

        if len(missing_test_fields):
            raise Exception(
                f"There are fields in ProductionSystem that might be tested in test_clean: {missing_test_fields}"
            )

        ps = ProductionSystemFactory(full=True, is_heating=False)
        ps.clean()
        self.assertIsNone(ps.efficiency_heating)
        self.assertIsNone(ps.enr_ratio_heating)
        self.assertIsNone(ps.investment_individual_heating)
        self.assertIsNone(ps.maintenance_individual_heating)
        self.assertIsNone(ps.investment_small_multi_unit_heating)
        self.assertIsNone(ps.maintenance_small_multi_unit_heating)
        self.assertIsNone(ps.provisions_small_multi_unit_heating)
        self.assertIsNone(ps.investment_medium_multi_unit_heating)
        self.assertIsNone(ps.maintenance_medium_multi_unit_heating)
        self.assertIsNone(ps.provisions_medium_multi_unit_heating)
        self.assertIsNone(ps.investment_large_multi_unit_heating)
        self.assertIsNone(ps.maintenance_large_multi_unit_heating)
        self.assertIsNone(ps.provisions_large_multi_unit_heating)

        ps = ProductionSystemFactory(full=True, is_hot_water=False)
        ps.clean()
        self.assertIsNone(ps.efficiency_hot_water)
        self.assertIsNone(ps.enr_ratio_hot_water)
        self.assertIsNone(ps.investment_individual_hot_water)
        self.assertIsNone(ps.maintenance_individual_hot_water)
        self.assertIsNone(ps.investment_small_multi_unit_hot_water)
        self.assertIsNone(ps.maintenance_small_multi_unit_hot_water)
        self.assertIsNone(ps.provisions_small_multi_unit_hot_water)
        self.assertIsNone(ps.investment_medium_multi_unit_hot_water)
        self.assertIsNone(ps.maintenance_medium_multi_unit_hot_water)
        self.assertIsNone(ps.provisions_medium_multi_unit_hot_water)
        self.assertIsNone(ps.investment_large_multi_unit_hot_water)
        self.assertIsNone(ps.maintenance_large_multi_unit_hot_water)
        self.assertIsNone(ps.provisions_large_multi_unit_hot_water)

        ps = ProductionSystemFactory(full=True, is_individual=False)
        ps.clean()
        self.assertIsNone(ps.investment_individual_heating)
        self.assertIsNone(ps.investment_individual_hot_water)
        self.assertIsNone(ps.maintenance_individual_heating)
        self.assertIsNone(ps.maintenance_individual_hot_water)

        ps = ProductionSystemFactory(full=True, is_multi_unit=False)
        ps.clean()
        self.assertIsNone(ps.investment_small_multi_unit_heating)
        self.assertIsNone(ps.investment_small_multi_unit_hot_water)
        self.assertIsNone(ps.maintenance_small_multi_unit_heating)
        self.assertIsNone(ps.maintenance_small_multi_unit_hot_water)
        self.assertIsNone(ps.provisions_small_multi_unit_heating)
        self.assertIsNone(ps.provisions_small_multi_unit_hot_water)
        self.assertIsNone(ps.investment_medium_multi_unit_heating)
        self.assertIsNone(ps.investment_medium_multi_unit_hot_water)
        self.assertIsNone(ps.maintenance_medium_multi_unit_heating)
        self.assertIsNone(ps.maintenance_medium_multi_unit_hot_water)
        self.assertIsNone(ps.provisions_medium_multi_unit_heating)
        self.assertIsNone(ps.provisions_medium_multi_unit_hot_water)
        self.assertIsNone(ps.investment_large_multi_unit_heating)
        self.assertIsNone(ps.investment_large_multi_unit_hot_water)
        self.assertIsNone(ps.maintenance_large_multi_unit_heating)
        self.assertIsNone(ps.maintenance_large_multi_unit_hot_water)
        self.assertIsNone(ps.provisions_large_multi_unit_heating)
        self.assertIsNone(ps.provisions_large_multi_unit_hot_water)

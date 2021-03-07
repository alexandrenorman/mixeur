from decimal import Decimal
from django.test import TestCase
from energies.models import CarbonTax
from energies.libs import get_carbon_taxes


class CarbonTaxesTestCase(TestCase):
    def setUp(self):
        CarbonTax.objects.all().delete()

        CarbonTax.objects.create(year=2022, amount=Decimal("86.2"))

    def test_get_carbon_taxes(self):
        ref_list = [
            {
                "year": 2022,
                "amount": Decimal("86.20"),
                "amount_with_tax": Decimal("103.44"),
            },
            {
                "year": 2023,
                "amount": Decimal("89.65"),
                "amount_with_tax": Decimal("107.58"),
            },
            {
                "year": 2024,
                "amount": Decimal("93.10"),
                "amount_with_tax": Decimal("111.72"),
            },
            {
                "year": 2025,
                "amount": Decimal("96.55"),
                "amount_with_tax": Decimal("115.86"),
            },
            {
                "year": 2026,
                "amount": Decimal("100.00"),
                "amount_with_tax": Decimal("120.00"),
            },
            {
                "year": 2027,
                "amount": Decimal("103.45"),
                "amount_with_tax": Decimal("124.14"),
            },
        ]

        computed_list = get_carbon_taxes(
            2022, 2028, {"year": 2026, "amount": Decimal("100.00")}
        )

        self.maxDiff = None
        self.assertListEqual(ref_list, computed_list)

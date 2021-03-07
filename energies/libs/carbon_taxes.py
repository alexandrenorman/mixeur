# -*- coding: utf-8 -*-
from decimal import Decimal
from energies.models import CarbonTax

TAX_AMOUNT = Decimal("1.2")


def get_carbon_taxes(start, end, custom_ref_tax):
    carbon_taxes = list(
        CarbonTax.objects.filter(year__gte=start, year__lte=end).values(
            "year", "amount"
        )
    )
    carbon_taxes.append(custom_ref_tax)
    years = [carbon_tax["year"] for carbon_tax in carbon_taxes]

    for year in range(start, end):

        if year in years:
            carbon_tax = [x for x in carbon_taxes if x["year"] == year][0]
        else:
            last_carbon_tax = [x for x in carbon_taxes if x["year"] == year - 1][0]
            if year < custom_ref_tax["year"]:
                amount = last_carbon_tax["amount"] + (
                    custom_ref_tax["amount"] - last_carbon_tax["amount"]
                ) / Decimal(custom_ref_tax["year"] - (year - 1))
            else:
                carbon_tax_ref_1 = [
                    x for x in carbon_taxes if x["year"] == custom_ref_tax["year"] - 3
                ][0]
                carbon_tax_ref_2 = [
                    x for x in carbon_taxes if x["year"] == custom_ref_tax["year"] - 2
                ][0]
                amount = last_carbon_tax["amount"] + (
                    carbon_tax_ref_2["amount"] - carbon_tax_ref_1["amount"]
                )

            carbon_tax = {"year": year, "amount": round(amount, 2)}
            carbon_taxes.append(carbon_tax)

        carbon_tax["amount_with_tax"] = round(carbon_tax["amount"] * TAX_AMOUNT, 2)

    carbon_taxes.sort(key=lambda x: x["year"])
    return carbon_taxes

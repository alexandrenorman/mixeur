# -*- coding: utf-8 -*-
from decimal import Decimal
from energies.models import Energy, YearlyEnergyPrice


def calculate_price_variation(energy_data, years_range, ref_year, yearly_energy_data):
    last_year = years_range[-1]
    avg_price_of_last_three_years = calculate_avg_price_of_last_three_years(
        yearly_energy_data
    )
    avg_price_from_ref_year = calculate_avg_price_from_ref_year(
        ref_year, yearly_energy_data
    )
    if avg_price_from_ref_year == 0:
        return 0

    return float(
        (
            Decimal(avg_price_of_last_three_years / avg_price_from_ref_year)
            ** Decimal(1 / ((last_year - 1) - ref_year - 1))
        )
        - 1
    )


def get_yearly_energies_prices(
    energies,
    years_range,
    is_collective=False,
    ref_year=2002,
    scenario="normal",
    price_variation_func=calculate_price_variation,
):
    """
    price_variation_func is used to determine price variation.
    Default case (autodiag copro) is the one defined in 'calculate_price_variation'
    """
    energies_data = Energy.objects.filter(identifier__in=energies)
    yearly_datum = list(
        YearlyEnergyPrice.objects.filter(
            energy__in=energies_data, year__range=years_range
        ).order_by("year")
    )

    series = []
    for energy_data in energies_data:
        ratio = energy_data.price_multi_unit_discount if is_collective else 1
        yearly_energy_data = [x for x in yearly_datum if x.energy_id == energy_data.pk]
        series.append(
            {
                "identifier": energy_data.identifier,
                "priceVariation": price_variation_func(
                    energy_data, years_range, ref_year, yearly_energy_data
                ),
                "yearlyPrices": [multiply(x.price, ratio) for x in yearly_energy_data],
            }
        )

    return series


def multiply(number, ratio):
    if number is None:
        return number
    else:
        return float(number * ratio)


def calculate_avg_price_of_last_three_years(yearly_energy_data):
    n = 0
    sum = 0
    for year_energy_data in yearly_energy_data[-3:]:
        price = year_energy_data.price
        if price is not None:
            n = n + 1
            sum = sum + price
    if n == 0:
        return 0
    else:
        return sum / n


def calculate_avg_price_from_ref_year(ref_year, yearly_energy_data):
    n = 0
    sum = 0
    for year_energy_data in yearly_energy_data:
        if year_energy_data.year in [ref_year - 1, ref_year, ref_year + 1]:
            price = year_energy_data.price
            if price is not None:
                n = n + 1
                sum = sum + price
    if n == 0:
        return 0
    else:
        return sum / n

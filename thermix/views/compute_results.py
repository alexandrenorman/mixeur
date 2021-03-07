# -*- coding: utf-8 -*-
import datetime
import json
from decimal import Decimal

from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse

from energies.libs import get_yearly_energies_prices
from helpers.views import ApiView
from thermix.libs import Compute


class DecimalToFloatJSONEncoder(DjangoJSONEncoder):
    """
    Used when returning data vith JSONResponse. All Decimal values are coerced as float
    """

    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super().default(obj)


def format_results(solutions):
    solutions_results = []

    series = {}
    series["period_cost_evolution_series"] = []
    series["environmental_indicators_series"] = []

    # carbon_tax = []  # THERMETRO-124
    combustible_cost = []
    maintenance_cost = []
    provisions_cost = []
    investment = []
    financial_support_amount = []
    period_total_cost_without_solar = []

    total_renewable_production = []
    renewable_heating_production = []
    renewable_heating_production_without_network = []
    renewable_heating_production_network_only = []
    total_renewable_production_without_network = []
    renewable_electricity = []
    primary_energy_consumption = []
    carbon_report = []
    carbon_report_km_equivalent = []

    for index, solution in enumerate(solutions):
        solutions_results.append(
            {
                "systems_labels": solution["systems_labels"],
                "systems_results": solution["systems_results"],
                "renewable_heating_production_ratio": float(
                    solution["environmental_indicators"][
                        "renewable_heating_production_ratio"
                    ]
                ),
                "renewable_production_ratio": float(
                    solution["environmental_indicators"]["renewable_production_ratio"]
                ),
                "period_total_cost": float(
                    solution["period_total_cost"]["overall_total"]
                ),
                "period_total_cost_by_year": float(
                    solution["period_total_cost"]["overall_total_by_year"]
                ),
                "primary_energy_consumption": float(
                    solution["environmental_indicators"]["primary_energy_consumption"]
                ),
                # "primary_energy_consumption_by_year": float(
                #     solution["environmental_indicators"][
                #         "primary_energy_consumption_by_year"
                #     ]
                # ),
                "final_energy_consumption": float(
                    solution["environmental_indicators"]["final_energy_consumption"]
                ),
                # "final_energy_consumption_by_year": float(
                #     solution["environmental_indicators"][
                #         "final_energy_consumption_by_year"
                #     ]
                # ),
                "carbon_report": float(
                    solution["environmental_indicators"]["carbon_report"]
                ),
                # "carbon_report_by_year": float(
                #     solution["environmental_indicators"]["carbon_report_by_year"]
                # ),
                "carbon_report_km_equivalent": float(
                    solution["environmental_indicators"]["carbon_report_km_equivalent"]
                ),
                # "carbon_report_km_equivalent_by_year": float(
                #     solution["environmental_indicators"][
                #         "carbon_report_km_equivalent_by_year"
                #     ]
                # ),
            }
        )

        period_total_cost = solution["period_total_cost"]
        # carbon_tax.append(float(period_total_cost["carbon_tax"]))  # THERMETRO-124
        combustible_cost.append(float(period_total_cost["combustible_cost"]))
        maintenance_cost.append(float(period_total_cost["maintenance_cost"]))
        provisions_cost.append(float(period_total_cost["provisions_cost"]))
        financial_support_amount_data = (
            float(period_total_cost["financial_support_amount"])
            if period_total_cost["financial_support_amount"] is not None
            else None
        )
        investment.append(float(period_total_cost["investment"]))
        financial_support_amount.append(financial_support_amount_data)
        period_total_cost_without_solar.append(
            float(solution["period_total_cost_without_solar"])
            if solution["period_total_cost_without_solar"] is not None
            else None
        )

        series["period_cost_evolution_series"].append(solution["period_cost_evolution"])

        environmental_indicators = solution["environmental_indicators"]
        total_renewable_production.append(
            float(environmental_indicators["total_renewable_production"])
        )
        renewable_heating_production.append(
            float(environmental_indicators["renewable_heating_production"])
        )
        renewable_heating_production_without_network.append(
            float(
                environmental_indicators["renewable_heating_production_without_network"]
            )
        )
        renewable_heating_production_network_only.append(
            float(environmental_indicators["renewable_heating_production_network_only"])
        )
        total_renewable_production_without_network.append(
            float(
                environmental_indicators["total_renewable_production_without_network"]
            )
        )
        renewable_electricity_data = (
            float(environmental_indicators["renewable_electricity"])
            if environmental_indicators["renewable_electricity"] is not None
            else None
        )
        renewable_electricity.append(renewable_electricity_data)
        primary_energy_consumption.append(
            float(environmental_indicators["primary_energy_consumption"])
        )
        carbon_report.append(float(environmental_indicators["carbon_report"]))

    series["period_total_cost_series"] = {
        # "carbon_tax": carbon_tax,  # THERMETRO-124
        "combustible_cost": combustible_cost,
        "maintenance_cost": maintenance_cost,
        "provisions_cost": provisions_cost,
        "investment": investment,
        "period_total_cost_without_solar": period_total_cost_without_solar,
        "financial_support_amount": financial_support_amount,
    }
    series["environmental_indicators_series"] = {
        "total_renewable_production": total_renewable_production,
        "renewable_heating_production": renewable_heating_production,
        "renewable_heating_production_without_network": renewable_heating_production_without_network,
        "renewable_heating_production_network_only": renewable_heating_production_network_only,
        "total_renewable_production_without_network": total_renewable_production_without_network,
        "renewable_electricity": renewable_electricity,
        "primary_energy_consumption": primary_energy_consumption,
        "carbon_report": carbon_report,
        "carbon_report_km_equivalent": carbon_report_km_equivalent,
    }

    return {"solutions_results": solutions_results, "series": series}


def get_price_variation_func(data):
    if data["metro_grenoble"]["enabled"]:
        return (
            lambda energy, *args: data["metro_grenoble"]["energies_overrided_data"]
            .get(energy.identifier, {})
            .get("price_variation")
        )
    return lambda energy, *args: energy.price_variation


class ComputeResultsView(ApiView):
    """
    ComputeResultsView
    """

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body, parse_float=Decimal)

        print("-- Compute Simulation Results --")
        print()
        computer = Compute(data)

        results = computer.compute_solutions()
        formatted_results = format_results(results)

        now = datetime.datetime.now()
        years = [now.year - 21, now.year - 1]
        energies = [
            "oil",
            "gaz_b1",
            "propane",
            "electricity",
            "wood",
            "shredded_wood",
            "bulk_granules",
            "bag_granules",
        ]
        is_multi_unit = data["needs"]["housing_category"] == "multi_unit"

        yearly_energies_prices_series = get_yearly_energies_prices(
            energies,
            years,
            is_multi_unit,
            price_variation_func=get_price_variation_func(data),
        )

        return JsonResponse(
            encoder=DecimalToFloatJSONEncoder,
            data={
                "solutions_results": formatted_results["solutions_results"],
                "period_total_cost_series": formatted_results["series"][
                    "period_total_cost_series"
                ],
                "period_cost_evolution_series": formatted_results["series"][
                    "period_cost_evolution_series"
                ],
                "environmental_indicators_series": formatted_results["series"][
                    "environmental_indicators_series"
                ],
                "yearly_energies_prices_series": yearly_energies_prices_series,
                "metro_grenoble_required_energy_prod": computer.metro_grenoble_energy_production_requirement(),
                "needs": data.get("needs"),
                "metro_grenoble": data.get("metro_grenoble"),
            },
        )

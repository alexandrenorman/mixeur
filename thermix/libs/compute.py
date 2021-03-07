# -*- coding: utf-8 -*-
import copy
from decimal import Decimal
from types import SimpleNamespace

from energies.models import ProductionSystem
from energies.models import SecondaryEfficiency

# from energies.libs import get_carbon_taxes # THERMETRO-124


THERMAL_SOLAR_MAX_PROD_RATIO = {
    "heating": Decimal("0.15"),
    "hot_water": Decimal("0.70"),
}

GHG_BY_CAR_RATIO = Decimal("0.217")


class Compute:
    def __init__(self, data):
        self.ref_year = data["year"]
        self.nb_years = 20
        self.needs = data["needs"]
        self.is_multi_unit = data["needs"]["housing_category"] == "multi_unit"
        self.dwellings_number = data["needs"].get("dwellings_number")
        self.heating_network_id = (
            ProductionSystem.objects.filter(identifier="heating_network")
            .values_list("id", flat=True)
            .first()
        )
        self.solutions = data["solutions"]
        # THERMETRO-124
        # self.carbon_taxes = get_carbon_taxes(
        #     self.ref_year - 1,
        #     self.ref_year + self.nb_years - 1,
        #     {
        #         "year": data["custom_carbon_tax"]["year"],
        #         "amount": Decimal(data["custom_carbon_tax"]["amount"]),
        #     },
        # )
        self.thermal_solar_prod_by_m2 = Decimal(data["thermal_solar_prod_by_m2"])
        metro_grenoble_data = data.get("metro_grenoble", {})
        self.metro_grenoble = SimpleNamespace(
            enabled=metro_grenoble_data.get("enabled", False),
            renovation_type=metro_grenoble_data.get("renovation_type", ""),
            floor_surface=Decimal(metro_grenoble_data.get("floor_surface", 0) or 0),
            ground_surface=Decimal(metro_grenoble_data.get("ground_surface", 0) or 0),
            required_energy_production_by_m2=Decimal(
                metro_grenoble_data.get("required_energy_production_by_m2", 20) or 20
            ),
        )

    @property
    def multiUnitSize(self) -> str:
        if not self.is_multi_unit or not self.dwellings_number:
            return None

        if self.dwellings_number < 50:
            return "small"
        if self.dwellings_number < 150:
            return "medium"
        return "large"

    def compute_solutions(self):
        solutions_results = []
        for solution in self.solutions:
            solution_results = self.compute_solution(solution)
            solutions_results.append(solution_results)

        return solutions_results

    def compute_solution(self, solution):
        if self.is_solution_contain_thermal_solar(solution):
            systems_results = self.compute_systems_thermal_solar(solution)
            total_costs_without_solar = self.solution_without_solar_total_cost(solution)
        else:
            systems_results = self.compute_systems(solution)
            total_costs_without_solar = None

        systems_labels = self.get_systems_labels_by_type(systems_results)
        return {
            "index": solution["index"],
            "systems_labels": systems_labels,
            "systems_results": systems_results,
            "period_total_cost": self.compute_period_total_cost(
                solution, systems_results
            ),
            "period_cost_evolution": self.compute_period_cost_evolution(
                solution, systems_results
            ),
            "environmental_indicators": self.compute_environmental_indicators(
                solution, systems_results
            ),
            "period_total_cost_without_solar": total_costs_without_solar,
        }

    def compute_systems(self, solution):
        systems_results = []
        for system_type in ["heating", "hot_water"]:
            for system_data in solution[system_type + "_systems"]:
                computed_system_data = self.compute_system(
                    system_type, system_data, solution=solution
                )
                if not computed_system_data:
                    continue
                systems_results.append({**system_data, **computed_system_data})

        return systems_results

    def compute_systems_thermal_solar(self, solution):
        systems_results = []
        consumed_solar_production = Decimal("0")

        # Important to start with hot water, because solar production is firstly used for hot water
        # then the remaining solar energy is used for heating (stored in consumed_solar_production)
        for system_type in ["hot_water", "heating"]:

            systems_data = self.ordered_systems_with_thermal_solar_first(
                solution[system_type + "_systems"]
            )

            if not systems_data:
                continue

            first_system_data = systems_data[0]

            if "is_thermal_solar" in first_system_data:
                computed_first_system_data = self.compute_thermal_solar_system(
                    system_type,
                    first_system_data,
                    consumed_solar_production,
                    solution=solution,
                )
                if not computed_first_system_data:
                    continue
                # consumed_solar_production will be passed to the other system AND to the heating in next loop
                consumed_solar_production = computed_first_system_data[
                    "solar_production"
                ]
            else:
                computed_first_system_data = self.compute_system(
                    system_type, first_system_data, solution=solution
                )
                consumed_solar_production = Decimal("0")

            systems_results.append({**first_system_data, **computed_first_system_data})

            if len(systems_data) == 2:
                other_system_data = systems_data[1]

                computed_other_system_data = self.compute_system(
                    system_type,
                    other_system_data,
                    consumed_solar_production,
                    solution=solution,
                )
                if not computed_other_system_data:
                    continue
                systems_results.append(
                    {**other_system_data, **computed_other_system_data}
                )

        return systems_results

    def compute_thermal_solar_system(
        self,
        system_type,
        system_data,
        consumed_solar_production=Decimal("0"),
        solution=None,
    ):
        if not system_data["production_system"]:
            return

        system = ProductionSystem.objects.get(pk=system_data["production_system"])
        label = system.get_identifier_display()

        solar_production = (
            self.thermal_solar_prod_by_m2 * system_data["solar_panels_surface"]
            - consumed_solar_production
        )

        max_prod_ratio = THERMAL_SOLAR_MAX_PROD_RATIO[system_type]

        used_solar_production = min(
            max_prod_ratio * self.needs[system_type], solar_production
        )
        solar_production = used_solar_production
        useful_heating_production = used_solar_production
        # useful_heating_production_by_year = useful_heating_production / self.nb_years
        renewable_heating_production = (
            used_solar_production  # consider enr ratio is 100% for thermal solar
        )

        combustible_costs = [Decimal("0") for year in range(1, self.nb_years + 1)]
        combustible_cost_by_year = Decimal("0")

        estimated_investment = (
            system_data["estimated_investment"] * system_data["solar_panels_surface"]
        )
        maintenance_cost = (
            system_data["maintenance_cost"] * system_data["solar_panels_surface"]
        )
        if self.is_multi_unit:
            provisions_cost = (
                system_data["provisions_cost"] * system_data["solar_panels_surface"]
            )
        else:
            provisions_cost = 0

        return {
            "type": system_type,
            "label": label,
            "identifier": system.identifier,
            "solar_production": solar_production,
            "useful_heating_production": useful_heating_production,
            # "useful_heating_production_by_year": useful_heating_production_by_year,
            "system_output_heating_production": Decimal("0"),
            "renewable_heating_production": renewable_heating_production,
            "final_energy_consumption": Decimal("0"),
            "final_energy_consumption_by_year": Decimal("0"),
            "primary_energy_consumption": Decimal("0"),
            "combustible_costs": combustible_costs,
            "combustible_cost_by_year": combustible_cost_by_year,
            "carbon_emission": Decimal("0"),
            "taxable_carbon_emission": 0,
            "secondary_efficiency": Decimal("0"),
            "estimated_investment": estimated_investment,
            "maintenance_cost": maintenance_cost,
            "provisions_cost": provisions_cost,
        }

    def compute_metro_grenoble_heating_network_system(
        self, system_type, system_data, avoided_production=Decimal("0"), solution=None
    ):

        system = ProductionSystem.objects.get(pk=system_data["production_system"])
        label = system.get_identifier_display()

        useful_heating_production = (
            Decimal(self.needs[system_type]) * Decimal(system_data["production_share"])
            - avoided_production
        )
        # Ensure production isn't negative (can occure if avoided_production is greater)
        useful_heating_production = max(useful_heating_production, Decimal("0"))
        # useful_heating_production_by_year = useful_heating_production / self.nb_years

        secondary_efficiency = SecondaryEfficiency.get(
            is_heating=(system_type == "heating"),
            is_multi_unit=self.is_multi_unit,
            is_hydro=system.is_hydro,
        )

        system_output_heating_production = (
            useful_heating_production / secondary_efficiency
        )
        efficiency = Decimal(system_data["efficiency"])

        if efficiency <= 0:
            final_energy_consumption = Decimal("0")
        else:
            final_energy_consumption = (
                # useful_heating_production / efficiency / secondary_efficiency
                system_output_heating_production
                / efficiency
            )

        final_energy_consumption_by_year = final_energy_consumption / self.nb_years

        primary_energy_consumption = (
            final_energy_consumption * system.energy.primary_energy_ratio
        )

        # if we are computing heating system and hot water is also heating network, use same uff as hot water system
        if system_type == "hot_water" or (
            len(solution["hot_water_systems"]) >= system_data["index"] + 1
            and solution["hot_water_systems"][system_data["index"]].get(
                "production_system"
            )
            == system_data["production_system"]
        ):
            uff_rate = Decimal("1.15")
        else:
            # So this case is when the system is only used for heating
            uff_rate = Decimal("1.05")

        reduction = Decimal("1")
        if system_output_heating_production >= Decimal("315000"):
            reduction = Decimal("0.88")
        if system_output_heating_production >= Decimal("1260000"):
            reduction = Decimal("0.76")

        maintenance_cost = (
            (system_output_heating_production * Decimal("34.02"))
            / uff_rate
            / Decimal("1000")
        ) * reduction

        connection_costs = {
            "small": Decimal("12953"),
            "medium": Decimal("15677"),
            "large": Decimal("22536"),
        }
        estimated_investment = connection_costs.get(self.multiUnitSize)

        combustible_costs_summer = (
            (Decimal("37.16") + Decimal("0.31"))
            * system_output_heating_production
            / Decimal("1000")
        )
        combustible_costs_winter = (
            (Decimal("46.71") + Decimal("0.31"))
            * system_output_heating_production
            / Decimal("1000")
        )

        combustible_cost_by_year = (combustible_costs_summer * Decimal("0.25")) + (
            combustible_costs_winter * Decimal("0.75")
        )

        # We force enr ratio (83%) for metro grenoble heating network
        enr_ratio = Decimal("0.83")
        renewable_heating_production = system_output_heating_production * enr_ratio

        # We force ghg_ratio 73.4gCO2/kWh for metro grenoble heating network
        ghg_ratio = Decimal("0.0734")
        carbon_emission = ghg_ratio * final_energy_consumption

        taxable_carbon_emission = 0
        if system.energy.combustible_category == "fossil":
            taxable_carbon_emission = carbon_emission

        energy_price = (
            combustible_cost_by_year
            / system_output_heating_production
            * Decimal("1000")
        )
        energy_price_variation = Decimal("0")

        combustible_costs = [combustible_cost_by_year] * self.nb_years

        return {
            "type": system_type,
            "label": label,
            "identifier": system.identifier,
            "renewable_heating_production": renewable_heating_production,
            "final_energy_consumption": final_energy_consumption,
            "final_energy_consumption_by_year": final_energy_consumption_by_year,
            "primary_energy_consumption": primary_energy_consumption,
            "carbon_emission": carbon_emission,
            "taxable_carbon_emission": taxable_carbon_emission,
            "secondary_efficiency": secondary_efficiency,
            "useful_heating_production": useful_heating_production,
            # "useful_heating_production_by_year": useful_heating_production_by_year,
            "system_output_heating_production": system_output_heating_production,
            "estimated_investment": estimated_investment,
            "maintenance_cost": maintenance_cost,
            "combustible_costs": combustible_costs,
            "energy_price": energy_price,  # Probably useless
            "energy_price_variation": energy_price_variation,  # Probably useless
        }

    def compute_system(
        self, system_type, system_data, avoided_production=Decimal("0"), solution=None
    ):
        if not system_data["production_system"]:
            return

        system = ProductionSystem.objects.get(pk=system_data["production_system"])

        if self.metro_grenoble.enabled and system.identifier == "heating_network":
            return self.compute_metro_grenoble_heating_network_system(
                system_type, system_data, avoided_production, solution
            )

        label = system.get_identifier_display()
        energy_price = Decimal(system_data["energy_price"])
        energy_price_variation = Decimal(system_data["energy_price_variation"])
        useful_heating_production = (
            Decimal(self.needs[system_type]) * Decimal(system_data["production_share"])
            - avoided_production
        )
        # Ensure production isn't negative (can occure if avoided_production is greater)
        useful_heating_production = max(useful_heating_production, Decimal("0"))
        # useful_heating_production_by_year = useful_heating_production / self.nb_years

        efficiency = Decimal(system_data["efficiency"])

        secondary_efficiency = SecondaryEfficiency.get(
            is_heating=(system_type == "heating"),
            is_multi_unit=self.is_multi_unit,
            is_hydro=system.is_hydro,
        )

        system_output_heating_production = (
            useful_heating_production / secondary_efficiency
        )

        if system.is_heat_pump:
            enr_ratio = system.get_heat_pump_enr_ratio(efficiency)
        elif system_type == "heating":
            enr_ratio = system.enr_ratio_heating
        else:
            enr_ratio = system.enr_ratio_hot_water

        renewable_heating_production = system_output_heating_production * (
            enr_ratio or Decimal("0")
        )

        if efficiency <= 0:
            final_energy_consumption = Decimal("0")
        else:
            final_energy_consumption = (
                # useful_heating_production / efficiency / secondary_efficiency
                system_output_heating_production
                / efficiency
            )
        final_energy_consumption_by_year = final_energy_consumption / self.nb_years

        primary_energy_consumption = (
            final_energy_consumption * system.energy.primary_energy_ratio
        )

        yearly_p1 = energy_price * final_energy_consumption / Decimal("100")

        combustible_costs = [
            yearly_p1 * (1 + energy_price_variation) ** (year - 1)
            for year in range(1, self.nb_years + 1)
        ]
        combustible_cost_by_year = sum(combustible_costs) / self.nb_years
        ghg_ratio = Decimal(system_data.get("ghg_ratio", system.energy.ghg_ratio))
        carbon_emission = ghg_ratio * final_energy_consumption
        taxable_carbon_emission = 0
        if system.energy.combustible_category == "fossil":
            taxable_carbon_emission = carbon_emission

        return {
            "type": system_type,
            "label": label,
            "identifier": system.identifier,
            "useful_heating_production": useful_heating_production,
            # "useful_heating_production_by_year": useful_heating_production_by_year,
            "system_output_heating_production": system_output_heating_production,
            "renewable_heating_production": renewable_heating_production,
            "final_energy_consumption": final_energy_consumption,
            "final_energy_consumption_by_year": final_energy_consumption_by_year,
            "primary_energy_consumption": primary_energy_consumption,
            "combustible_costs": combustible_costs,
            "combustible_cost_by_year": combustible_cost_by_year,
            "carbon_emission": carbon_emission,
            "taxable_carbon_emission": taxable_carbon_emission,
            "secondary_efficiency": secondary_efficiency,
        }

    def get_systems_labels_by_type(self, systems_results):
        systems_labels = {"heating": [], "hot_water": []}
        for system_results in systems_results:
            systems_labels[system_results["type"]].append(system_results["label"])
        return systems_labels

    def ordered_systems_with_thermal_solar_first(self, systems_data):
        if not systems_data:
            return systems_data
        system = ProductionSystem.objects.get(pk=systems_data[0]["production_system"])
        if system.is_thermal_solar:
            systems_data[0]["is_thermal_solar"] = True
            return systems_data
        elif len(systems_data) == 2:
            system2 = ProductionSystem.objects.get(
                pk=systems_data[1]["production_system"]
            )
            if system2.is_thermal_solar:
                systems_data[1]["is_thermal_solar"] = True
                return (systems_data[1], systems_data[0])
        return systems_data

    def is_solution_contain_thermal_solar(self, solution):
        for system_type in ["heating", "hot_water"]:
            for system_data in solution[system_type + "_systems"]:
                if not system_data["production_system"]:
                    continue
                system = ProductionSystem.objects.get(
                    pk=system_data["production_system"]
                )
                if system and system.is_thermal_solar:
                    return True
        return False

    def solution_without_solar(self, solution):
        # Make a copy of solution
        solution_without_solar = copy.deepcopy(solution)

        # Remove solar production systems
        # Set other systems to share 100%
        for system_type in ["heating", "hot_water"]:
            for system_data in solution_without_solar[system_type + "_systems"]:
                if not system_data["production_system"]:
                    continue
                system = ProductionSystem.objects.get(
                    pk=system_data["production_system"]
                )
                if system and system.is_thermal_solar:
                    system_data["production_system"] = 0
                else:
                    system_data["production_share"] = 1

        return solution_without_solar

    def solution_without_solar_total_cost(self, solution):
        solution_without_solar = self.solution_without_solar(solution)
        # solution_without_solar_results = self.compute_solution(solution_without_solar)
        systems_results = self.compute_systems(solution_without_solar)
        return sum(
            [
                value
                for value in self.compute_period_total_cost(
                    solution, systems_results
                ).values()
                if value
            ]
        )

    def compute_period_total_cost(self, solution, systems_results):
        combustible_cost = sum([sum(x["combustible_costs"]) for x in systems_results])
        # THERMETRO-124
        # total_carbon_emission = Decimal(
        #     sum([x["taxable_carbon_emission"] for x in systems_results])
        # )
        # carbon_tax = sum(
        #     [
        #         total_carbon_emission / Decimal("1000") * carbon_tax["amount_with_tax"]
        #         for carbon_tax in self.carbon_taxes
        #     ]
        # )

        maintenance_cost = 0
        provisions_cost = 0
        investment = 0
        for system_data in systems_results:
            investment += system_data["estimated_investment"]
            maintenance_cost += system_data["maintenance_cost"] * self.nb_years
            if self.is_multi_unit:
                provisions_cost += system_data["provisions_cost"] * self.nb_years

        financial_support_amount = None
        if solution["financial_support"]:
            financial_support_amount = solution["financial_support_amount"]
            investment = max(Decimal("0"), investment - financial_support_amount)

        overall_total = sum(
            (
                # carbon_tax, # THERMETRO-124
                combustible_cost,
                maintenance_cost,
                provisions_cost,
                investment,
            )
        )
        overall_total_by_year = overall_total / self.nb_years

        return {
            # "carbon_tax": carbon_tax, # THERMETRO-124
            "combustible_cost": combustible_cost,
            "maintenance_cost": maintenance_cost,
            "provisions_cost": provisions_cost,
            "investment": investment,
            "financial_support_amount": financial_support_amount,
            "overall_total": overall_total,
            "overall_total_by_year": overall_total_by_year,
        }

    def compute_period_cost_evolution(self, solution, systems_results):
        maintenance_cost = 0
        provisions_cost = 0
        investment = 0
        for system_data in systems_results:
            investment += system_data["estimated_investment"]
            maintenance_cost += system_data["maintenance_cost"]
            if self.is_multi_unit:
                provisions_cost += system_data["provisions_cost"]

        series = []

        if solution["financial_support"]:
            investment = max(
                Decimal("0"), investment - solution["financial_support_amount"]
            )

        # Investment only on first year
        cumulated_cost = investment

        i = 1
        while i <= 20:
            combustible_cost = sum(
                [x["combustible_costs"][i - 1] for x in systems_results]
            )
            # THERMETRO-124
            # carbon_tax = (
            #     Decimal(sum([x["taxable_carbon_emission"] for x in systems_results]))
            #     / Decimal("1000")
            #     * self.carbon_taxes[i - 1]["amount_with_tax"]
            # )

            cumulated_cost += (
                # combustible_cost + carbon_tax + maintenance_cost + provisions_cost # THERMETRO-124
                combustible_cost
                + maintenance_cost
                + provisions_cost
            )
            series.append(
                {"year": self.ref_year + i - 1, "cumulated_cost": cumulated_cost}
            )

            i += 1

        return series

    def compute_environmental_indicators(self, solution, systems_results):
        primary_energy_consumption = 0
        final_energy_consumption = 0
        carbon_report = 0
        carbon_report_km_equivalent = 0
        renewable_heating_production = 0
        renewable_heating_production_without_network = 0
        renewable_heating_production_network_only = 0
        total_heating_energy_production = 0
        for system_result in systems_results:
            primary_energy_consumption += system_result["primary_energy_consumption"]
            final_energy_consumption += system_result["final_energy_consumption"]
            carbon_report += system_result["carbon_emission"]
            total_heating_energy_production += system_result[
                "system_output_heating_production"
            ]
            renewable_heating_production += system_result[
                "renewable_heating_production"
            ]
            if system_result["production_system"] == self.heating_network_id:
                renewable_heating_production_network_only += system_result[
                    "renewable_heating_production"
                ]
            else:
                renewable_heating_production_without_network += system_result[
                    "renewable_heating_production"
                ]

        # primary_energy_consumption_by_year = primary_energy_consumption / self.nb_years
        # final_energy_consumption_by_year = final_energy_consumption / self.nb_years
        # carbon_report_by_year = carbon_report / self.nb_years
        carbon_report_km_equivalent = carbon_report * GHG_BY_CAR_RATIO
        # carbon_report_km_equivalent_by_year = (
        #     carbon_report_km_equivalent / self.nb_years
        # )

        renewable_electricity = None
        if solution["renewable_electricity"]:
            renewable_electricity = solution["renewable_electricity_production"]

        if total_heating_energy_production == 0:
            renewable_heating_production_ratio = 0
        else:
            renewable_heating_production_ratio = (
                renewable_heating_production / total_heating_energy_production
            )
        total_renewable_production = renewable_heating_production + (
            renewable_electricity or 0
        )
        total_renewable_production_without_network = (
            renewable_heating_production_without_network + (renewable_electricity or 0)
        )

        total_energy_production = total_heating_energy_production + (
            renewable_electricity or 0
        )
        if total_energy_production == 0:
            renewable_production_ratio = 0
        else:
            renewable_production_ratio = (
                total_renewable_production / total_energy_production
            )

        return {
            "renewable_production_ratio": renewable_production_ratio,
            "renewable_heating_production_ratio": renewable_heating_production_ratio,
            "total_renewable_production": total_renewable_production,
            "total_renewable_production_without_network": total_renewable_production_without_network,
            "renewable_heating_production": renewable_heating_production,
            "renewable_heating_production_without_network": renewable_heating_production_without_network,
            "renewable_heating_production_network_only": renewable_heating_production_network_only,
            "renewable_electricity": renewable_electricity,
            "primary_energy_consumption": primary_energy_consumption,
            # "primary_energy_consumption_by_year": primary_energy_consumption_by_year,
            "final_energy_consumption": final_energy_consumption,
            # "final_energy_consumption_by_year": final_energy_consumption_by_year,
            "carbon_report": carbon_report,
            # "carbon_report_by_year": carbon_report_by_year,
            "carbon_report_km_equivalent": carbon_report_km_equivalent,
            # "carbon_report_km_equivalent_by_year": carbon_report_km_equivalent_by_year,
        }

    def metro_grenoble_energy_production_requirement(self):
        if (
            self.metro_grenoble.enabled
            and self.metro_grenoble.renovation_type == "new_building"
            and self.metro_grenoble.floor_surface > Decimal("1000")
            and self.metro_grenoble.ground_surface
            and self.metro_grenoble.required_energy_production_by_m2
        ):
            return (
                self.metro_grenoble.ground_surface
                * self.metro_grenoble.required_energy_production_by_m2
            )
        return None

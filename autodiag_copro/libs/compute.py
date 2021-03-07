# -*- coding: utf-8 -*-
from decimal import Decimal
from functools import reduce
from helpers.forms import FormProxy

from autodiag_copro.forms import CoproForm, RawYearlyDataForm


def build_years(last_year):
    years = []
    for i in range(6):
        ending = last_year - i
        beginning = ending - 1
        years.append(f"{beginning}-{ending}")
    return years


class Compute:
    def __init__(self, data, params):
        self.general_infos = self.__general_infos(data)
        self.main_params = params["main_params"]
        self.yearly_main_params = params["yearly_main_params"]
        self.combustible_params = params["combustible_params"]
        self.yearly_combustible_params = params["yearly_combustible_params"]
        self.yearly_datum = data["yearly_data"]["yearly_datum"]
        self.years = build_years(data["diagnostic"]["last_year"])
        self.yearly_results = list(
            map(lambda x: self.__compute_yearly_results(x), self.years)
        )
        self.avg_energy = self.__compute_avg_energy()
        self.ref_avg_energy = self.__compute_ref_avg_energy("efficient")

    def __general_infos(self, data):
        general_infos_form = CoproForm(data["general_infos"])
        general_infos_form.is_valid()
        return FormProxy(general_infos_form)

    def __compute_yearly_results(self, years):
        refs = self.__compute_refs(years)
        yearly_data = [y for y in self.yearly_datum if y["years"] == years][0]
        yearly_data_form = RawYearlyDataForm(yearly_data)
        if yearly_data_form.is_valid():
            data = FormProxy(yearly_data_form)
            results = self.__compute_results(data)
            saves = self.__compute_saves(data, refs["efficient"], results)
        else:
            results = {}
            saves = {}

        return {"years": years, "refs": refs, "results": results, "saves": saves}

    def __compute_refs(self, years):
        general_infos = self.general_infos
        main_params = self.main_params
        yearly_main_params = [x for x in self.yearly_main_params if x.years == years][0]
        combustible_params = self.combustible_params
        yearly_combustible_params = [
            x for x in self.yearly_combustible_params if x.years == years
        ][0]

        ref_avg_energy = 175 * (
            general_infos.altitude.value + general_infos.climatic_zone.value
        )
        ref_eff_energy = 80 * (
            general_infos.altitude.value + general_infos.climatic_zone.value
        )
        ref_avg_energy_hot_water = (
            main_params.avg_hot_water_conso_ratio
            * combustible_params.avg_hot_water_energy_ratio
            / main_params.avg_living_area
        )
        ref_eff_energy_hot_water = (
            main_params.eff_hot_water_conso_ratio
            * combustible_params.eff_hot_water_energy_ratio
            / main_params.avg_living_area
        )
        ref_avg_energy_heating = ref_avg_energy - ref_avg_energy_hot_water
        ref_eff_energy_heating = ref_eff_energy - ref_eff_energy_hot_water

        ref_avg_charges = (
            ref_avg_energy
            * yearly_combustible_params.avg_energy_cost_ratio
            * Decimal(0.01)
        )
        ref_eff_charges = (
            ref_eff_energy
            * yearly_combustible_params.eff_energy_cost_ratio
            * Decimal(0.01)
        )
        ref_avg_charges_heating = ref_avg_charges - (
            Decimal(0.01)
            * (
                main_params.avg_hot_water_conso_ratio
                * combustible_params.avg_hot_water_energy_ratio
                * yearly_combustible_params.avg_energy_cost_ratio
                * general_infos.number_of_dwellings
            )
            / general_infos.living_area
        )
        ref_eff_charges_heating = ref_eff_charges - (
            Decimal(0.01)
            * (
                main_params.eff_hot_water_conso_ratio
                * combustible_params.eff_hot_water_energy_ratio
                * yearly_combustible_params.eff_energy_cost_ratio
                * general_infos.number_of_dwellings
            )
            / general_infos.living_area
        )
        ref_avg_charges_hot_water = (
            yearly_combustible_params.avg_energy_cost_ratio
            * Decimal(0.01)
            * combustible_params.avg_hot_water_energy_ratio
            + yearly_main_params.water_cost
        )
        ref_eff_charges_hot_water = (
            yearly_combustible_params.eff_energy_cost_ratio
            * Decimal(0.01)
            * combustible_params.eff_hot_water_energy_ratio
            + yearly_main_params.water_cost
        )

        return {
            "average": {
                "energy_heating_hot_water": ref_avg_energy,
                "energy_heating": ref_avg_energy_heating,
                "energy_hot_water": ref_avg_energy_hot_water,
                "charges_heating_hot_water": ref_avg_charges,
                "charges_heating": ref_avg_charges_heating,
                "charges_hot_water": ref_avg_charges_hot_water,
                "energy_hot_water_ratio": combustible_params.avg_hot_water_energy_ratio,
                "energy_cost_ratio": yearly_combustible_params.avg_energy_cost_ratio,
                "water_conso_ratio": main_params.avg_water_conso_ratio,
                "hot_water_conso_ratio": main_params.avg_hot_water_conso_ratio,
            },
            "efficient": {
                "energy_heating_hot_water": ref_eff_energy,
                "energy_heating": ref_eff_energy_heating,
                "energy_hot_water": ref_eff_energy_hot_water,
                "charges_heating_hot_water": ref_eff_charges,
                "charges_heating": ref_eff_charges_heating,
                "charges_hot_water": ref_eff_charges_hot_water,
                "energy_hot_water_ratio": combustible_params.eff_hot_water_energy_ratio,
                "energy_cost_ratio": yearly_combustible_params.eff_energy_cost_ratio,
                "water_conso_ratio": main_params.eff_water_conso_ratio,
                "hot_water_conso_ratio": main_params.eff_hot_water_conso_ratio,
            },
        }

    def __compute_results(self, yearly_data):  # noqa: C901
        general_infos = self.general_infos

        if general_infos.with_dju_correction:
            ratio_dju_correction = (
                Decimal(general_infos.ref_dju_correction) / yearly_data.dju_correction
            )
        else:
            ratio_dju_correction = 1
        if general_infos.hot_water_is_collective:
            hot_water_energy_charges = yearly_data.hot_water_energy_charges
            hot_water_consumption = yearly_data.hot_water_consumption
            hot_water_consumption_charges = yearly_data.hot_water_consumption_charges
        else:
            hot_water_energy_charges = Decimal(0)
            hot_water_consumption = Decimal(0)
            hot_water_consumption_charges = Decimal(0)

        if general_infos.water_is_collective:
            water_consumption = yearly_data.water_consumption
        else:
            water_consumption = Decimal(0)
        # CHARGES
        # consumption_charges = (
        #     yearly_data.hot_water_consumption_charges
        #     + yearly_data.water_consumption_charges
        # )
        if general_infos.heating_combustible == 1:  # Fioul
            energy_consumption = Decimal(9.97) * yearly_data.energy_consumption
        elif general_infos.heating_combustible == 2:  # Gaz de ville
            energy_consumption = Decimal(0.9) * yearly_data.energy_consumption
        elif general_infos.heating_combustible == 3:  # Gaz Propane
            energy_consumption = Decimal(13.8) * yearly_data.energy_consumption
        elif general_infos.heating_combustible == 4:  # Réseau de chaleur
            energy_consumption = Decimal(1) * yearly_data.energy_consumption
        elif general_infos.heating_combustible == 5:  # Électricité
            energy_consumption = Decimal(1) * yearly_data.energy_consumption
        elif general_infos.heating_combustible == 6:  # Bois granulés
            energy_consumption = Decimal(4.6) * yearly_data.energy_consumption

        energy_charges = yearly_data.heating_energy_charges + hot_water_energy_charges
        heating_energy_consumption_charges_with_dju_correction = (
            ratio_dju_correction * yearly_data.heating_energy_charges
        )
        energy_consumption_charges_with_dju_correction = (
            heating_energy_consumption_charges_with_dju_correction
            + hot_water_energy_charges
        )
        # CONSUMPTIONS
        energy_cost_ratio = energy_charges / energy_consumption * 100
        heating_energy_consumption = yearly_data.heating_energy_charges / (
            Decimal(0.01) * energy_cost_ratio
        )
        heating_energy_consumption_with_dju_correction = (
            heating_energy_consumption_charges_with_dju_correction
            / (Decimal(0.01) * energy_cost_ratio)
        )
        hot_water_energy_consumption = hot_water_energy_charges / (
            Decimal(0.01) * energy_cost_ratio
        )
        energy_consumption_with_dju_correction = (
            heating_energy_consumption_with_dju_correction
            + hot_water_energy_consumption
        )

        # YEARLY RESULTS
        energy_heating_hot_water = (
            energy_consumption_with_dju_correction / general_infos.living_area
        )
        raw_energy_heating = heating_energy_consumption / general_infos.living_area
        energy_heating = (
            heating_energy_consumption_with_dju_correction / general_infos.living_area
        )
        energy_hot_water = hot_water_energy_consumption / general_infos.living_area

        charges_heating_hot_water = (
            energy_consumption_charges_with_dju_correction
            + hot_water_consumption_charges
        ) / general_infos.living_area
        charges_heating = (
            heating_energy_consumption_charges_with_dju_correction
            / general_infos.living_area
        )

        if general_infos.hot_water_is_collective:
            charges_hot_water = (
                hot_water_energy_charges + hot_water_consumption_charges
            ) / hot_water_consumption

            energy_hot_water_ratio = hot_water_energy_charges / (
                energy_cost_ratio * Decimal(0.01) * hot_water_consumption
            )
        else:
            charges_hot_water = 0
            energy_hot_water_ratio = 0

        hot_water_conso_ratio = (
            hot_water_consumption / general_infos.number_of_dwellings
        )
        water_conso_ratio = water_consumption / general_infos.number_of_dwellings

        return {
            "energy_consumption_with_dju_correction": energy_consumption_with_dju_correction,
            "energy_heating_hot_water": energy_heating_hot_water,
            "raw_energy_heating": raw_energy_heating,
            "energy_heating": energy_heating,
            "energy_hot_water": energy_hot_water,
            "charges_heating_hot_water": charges_heating_hot_water,
            "charges_heating": charges_heating,
            "charges_hot_water": charges_hot_water,
            "energy_hot_water_ratio": energy_hot_water_ratio,
            "energy_cost_ratio": energy_cost_ratio,
            "water_conso_ratio": water_conso_ratio,
            "hot_water_conso_ratio": hot_water_conso_ratio,
        }

    def __compute_saves(self, yearly_data, ref, yearly_results):  # noqa: C901
        general_infos = self.general_infos

        saves = {"percent": {}, "money": {}}
        for key, value in yearly_results.items():
            if key in ["energy_consumption_with_dju_correction", "raw_energy_heating"]:
                continue
            elif value <= 0:
                saves["percent"][key] = 0
                saves["money"][key] = 0
            else:
                saves["percent"][key] = max((value - ref[key]) / value, Decimal(0))
                if key in [
                    "energy_heating_hot_water",
                    "energy_heating",
                    "energy_hot_water",
                ]:
                    saves["money"][key] = (
                        (value - ref[key])
                        * general_infos.living_area
                        * yearly_results["energy_cost_ratio"]
                        * Decimal(0.01)
                    )
                elif key in ["charges_heating_hot_water", "charges_heating"]:
                    saves["money"][key] = (value - ref[key]) * general_infos.living_area
                elif key == "charges_hot_water":
                    saves["money"][key] = (
                        value - ref[key]
                    ) * yearly_data.hot_water_consumption
                elif key == "energy_hot_water_ratio":
                    saves["money"][key] = (
                        (value - ref[key])
                        * yearly_results["energy_cost_ratio"]
                        * yearly_data.hot_water_consumption
                        * Decimal(0.01)
                    )
                elif key == "energy_cost_ratio":
                    saves["money"][key] = (
                        (value - ref[key])
                        * yearly_results["energy_heating_hot_water"]
                        * general_infos.living_area
                        * Decimal(0.01)
                    )
                elif key == "water_conso_ratio":
                    saves["money"][key] = (
                        (value - ref[key])
                        * (
                            yearly_data.water_consumption_charges
                            / yearly_data.water_consumption
                        )
                        * general_infos.number_of_dwellings
                    )
                elif key == "hot_water_conso_ratio":
                    saves["money"][key] = (
                        (value - ref[key])
                        * yearly_results["charges_hot_water"]
                        * general_infos.number_of_dwellings
                    )
                saves["money"][key] = max(saves["money"][key], Decimal(0))

        return saves

    def __compute_avg_energy(self):
        energy_consumptions = []
        for year_results in self.yearly_results:
            results = year_results["results"]
            if len(results) > 0:
                energy_consumptions.append(
                    results["energy_consumption_with_dju_correction"]
                )
        avg_energy_consumption = reduce(
            (lambda x, y: x + y), energy_consumptions
        ) / len(energy_consumptions)
        return avg_energy_consumption / self.general_infos.living_area

    def __compute_ref_avg_energy(self, ref):
        avg_energy_consumption = reduce(
            (lambda x, y: x + y),
            list(
                map(
                    lambda x: x["refs"][ref]["energy_heating_hot_water"],
                    self.yearly_results,
                )
            ),
        ) / len(self.yearly_results)
        return avg_energy_consumption

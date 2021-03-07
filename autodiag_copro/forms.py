# -*- coding: utf-8 -*-
from django import forms

from .models import (
    Params,
    YearlyParams,
    DefaultParams,
    DefaultYearlyParams,
    CombustibleParams,
    YearlyCombustibleParams,
    DefaultCombustibleParams,
    DefaultYearlyCombustibleParams,
    Copro,
    YearlyData,
    Diagnostic,
)


class ParamsForm(forms.ModelForm):
    class Meta:
        model = Params
        fields = (
            "avg_living_area",
            "avg_hot_water_conso_ratio",
            "avg_water_conso_ratio",
            "eff_hot_water_conso_ratio",
            "eff_water_conso_ratio",
            "eff_water_conso_ratio",
        )


class DefaultParamsForm(forms.ModelForm):
    class Meta:
        model = DefaultParams
        fields = (
            "key",
            "avg_living_area",
            "avg_hot_water_conso_ratio",
            "avg_water_conso_ratio",
            "eff_hot_water_conso_ratio",
            "eff_water_conso_ratio",
        )


class YearlyParamsForm(forms.ModelForm):
    class Meta:
        model = YearlyParams
        fields = ("params", "years", "water_cost")


class DefaultYearlyParamsForm(forms.ModelForm):
    class Meta:
        model = DefaultYearlyParams
        fields = ("params", "years", "water_cost")


class CombustibleParamsForm(forms.ModelForm):
    class Meta:
        model = CombustibleParams
        fields = (
            "params",
            "combustible",
            "avg_hot_water_energy_ratio",
            "eff_hot_water_energy_ratio",
        )


class DefaultCombustibleParamsForm(forms.ModelForm):
    class Meta:
        model = DefaultCombustibleParams
        fields = (
            "params",
            "combustible",
            "avg_hot_water_energy_ratio",
            "eff_hot_water_energy_ratio",
        )


class YearlyCombustibleParamsForm(forms.ModelForm):
    class Meta:
        model = YearlyCombustibleParams
        fields = (
            "combustible_params",
            "years",
            "avg_energy_cost_ratio",
            "eff_energy_cost_ratio",
        )


class DefaultYearlyCombustibleParamsForm(forms.ModelForm):
    class Meta:
        model = DefaultYearlyCombustibleParams
        fields = (
            "combustible_params",
            "years",
            "avg_energy_cost_ratio",
            "eff_energy_cost_ratio",
        )


class CoproForm(forms.ModelForm):
    class Meta:
        model = Copro
        fields = (
            "name",
            "address",
            "climatic_zone",
            "altitude",
            "number_of_dwellings",
            "number_of_offices_shops",
            "living_area",
            "number_of_buildings",
            "number_of_floors",
            "syndic_name",
            "build_year",
            "heating_is_collective",
            "heating_individualisation_mode",
            "heating_individualisation_costs",
            "heating_has_maintenance_contract_P2",
            "heating_maintenance_contract_P2_cost",
            "heating_has_maintenance_contract_P2_P3",
            "heating_maintenance_contract_P2_P3_cost",
            "heating_combustible",
            "hot_water_is_collective",
            "hot_water_has_meters",
            "water_is_collective",
            "water_has_meters",
            "with_dju_correction",
            "ref_dju_correction",
        )


class YearlyDataForm(forms.ModelForm):
    class Meta:
        model = YearlyData
        fields = (
            "copro",
            "years",
            "heating_energy_charges",
            "energy_consumption",
            "hot_water_energy_charges",
            "hot_water_consumption_charges",
            "hot_water_consumption",
            "water_consumption_charges",
            "water_consumption",
            "dju_correction",
        )


class RawYearlyDataForm(forms.ModelForm):
    class Meta:
        model = YearlyData
        fields = (
            "years",
            "heating_energy_charges",
            "energy_consumption",
            "hot_water_energy_charges",
            "hot_water_consumption_charges",
            "hot_water_consumption",
            "water_consumption_charges",
            "water_consumption",
            "dju_correction",
        )


class DiagnosticForm(forms.ModelForm):
    class Meta:
        model = Diagnostic
        fields = ("id", "last_year", "user", "advisor", "copro", "params", "comments")

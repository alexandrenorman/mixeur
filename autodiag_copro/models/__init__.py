# -*- coding: utf-8 -*-
from .diagnostic import Diagnostic
from .copro import Copro
from .yearly_data import YearlyData
from .params import DefaultParams, Params
from .yearly_params import DefaultYearlyParams, YearlyParams
from .combustible_params import DefaultCombustibleParams, CombustibleParams
from .yearly_combustible_params import (
    DefaultYearlyCombustibleParams,
    YearlyCombustibleParams,
)
from .climatic_zone_ratio import ClimaticZoneRatio
from .altitude_ratio import AltitudeRatio

__all__ = [
    "Diagnostic",
    "Copro",
    "YearlyData",
    "DefaultParams",
    "DefaultYearlyParams",
    "Params",
    "YearlyParams",
    "DefaultCombustibleParams",
    "DefaultYearlyCombustibleParams",
    "CombustibleParams",
    "YearlyCombustibleParams",
    "ClimaticZoneRatio",
    "AltitudeRatio",
]

# -*- coding: utf-8 -*-
import serpy
import time

from accounts.serializers import UserSimpleSerializer


class PhoneField(serpy.Field):
    def to_value(self, value):
        if isinstance(value, str):
            return value
        else:
            return f"(+{value.country_code}) {value.national_number}"


class AbstractYearlyParamsSerializer(serpy.Serializer):
    years = serpy.StrField()
    water_cost = serpy.FloatField()


class YearlyParamsSerializer(AbstractYearlyParamsSerializer):
    pk = serpy.IntField()


class DefaultYearlyParamsSerializer(AbstractYearlyParamsSerializer):
    pk = serpy.IntField()


class AbstractParamsSerializer(serpy.Serializer):
    avg_living_area = serpy.IntField()
    # AVERAGE
    avg_hot_water_conso_ratio = serpy.FloatField()
    avg_water_conso_ratio = serpy.FloatField()
    # EFFICIENT
    eff_hot_water_conso_ratio = serpy.FloatField()
    eff_water_conso_ratio = serpy.FloatField()

    yearly_params = AbstractYearlyParamsSerializer(
        required=True, many=True, attr="yearly_params.all", call=True
    )


class ParamsSerializer(AbstractParamsSerializer):
    pk = serpy.IntField()

    yearly_params = YearlyParamsSerializer(
        required=True, many=True, attr="yearly_params.all", call=True
    )


class DefaultParamsSerializer(AbstractParamsSerializer):
    pk = serpy.IntField()
    key = serpy.IntField(required=False)

    yearly_params = YearlyParamsSerializer(
        required=True, many=True, attr="yearly_params.all", call=True
    )


class AbstractYearlyCombustibleParamsSerializer(serpy.Serializer):
    years = serpy.Field()

    avg_energy_cost_ratio = serpy.FloatField()
    eff_energy_cost_ratio = serpy.FloatField()


class YearlyCombustibleParamsSerializer(AbstractYearlyCombustibleParamsSerializer):
    pk = serpy.IntField()


class DefaultYearlyCombustibleParamsSerializer(
    AbstractYearlyCombustibleParamsSerializer
):
    pk = serpy.IntField()


class YearlyCombustibleParamsIdsSerializer(serpy.Serializer):
    pk = serpy.IntField()


class AbstractCombustibleParamsSerializer(serpy.Serializer):
    combustible = serpy.IntField()

    avg_hot_water_energy_ratio = serpy.FloatField()
    eff_hot_water_energy_ratio = serpy.FloatField()


class CombustibleParamsSerializer(AbstractCombustibleParamsSerializer):
    pk = serpy.IntField()

    yearly_combustible_params_ids = serpy.MethodField()

    def get_yearly_combustible_params_ids(self, obj):
        return list(obj.yearly_combustible_params.values_list("id", flat=True))


class DefaultCombustibleParamsSerializer(CombustibleParamsSerializer):
    pk = serpy.IntField()


class AbstractCombustibleParamsWithYearlySerializer(
    AbstractCombustibleParamsSerializer
):
    yearly_combustible_params = AbstractYearlyCombustibleParamsSerializer(
        required=True, many=True, attr="yearly_combustible_params.all", call=True
    )


class AbstractYearlyDataSerializer(serpy.Serializer):
    years = serpy.StrField()

    # HEATING
    heating_energy_charges = serpy.FloatField()
    energy_consumption = serpy.FloatField()

    # HOTWATER
    hot_water_energy_charges = serpy.FloatField(required=False)
    hot_water_consumption_charges = serpy.FloatField(required=False)
    hot_water_consumption = serpy.FloatField(required=False)

    # WATER
    water_consumption_charges = serpy.FloatField(required=False)
    water_consumption = serpy.FloatField(required=False)

    # DJU
    dju_correction = serpy.IntField(required=False)


class YearlyDataSerializer(AbstractYearlyDataSerializer):
    pk = serpy.IntField()


class AltitudeRatioSerializer(serpy.Serializer):
    pk = serpy.IntField()

    altitude = serpy.IntField()
    value = serpy.FloatField()


class ClimaticZoneRatioSerializer(serpy.Serializer):
    code = serpy.IntField()

    name = serpy.StrField()
    value = serpy.FloatField()


class AbstractCoproSerializer(serpy.Serializer):
    name = serpy.StrField()
    address = serpy.StrField()

    # COPRO DESCRIPTION
    number_of_dwellings = serpy.IntField()
    number_of_offices_shops = serpy.IntField(required=False)
    living_area = serpy.IntField()
    number_of_buildings = serpy.IntField(required=False)
    number_of_floors = serpy.IntField(required=False)
    syndic_name = serpy.StrField()
    build_year = serpy.IntField()

    # HEATING INFOS
    heating_is_collective = serpy.BoolField()
    heating_individualisation_mode = serpy.IntField()
    heating_individualisation_costs = serpy.FloatField(required=False)
    heating_has_maintenance_contract_P2 = serpy.BoolField()
    heating_maintenance_contract_P2_cost = serpy.FloatField(required=False)
    heating_has_maintenance_contract_P2_P3 = serpy.BoolField()
    heating_maintenance_contract_P2_P3_cost = serpy.FloatField(required=False)
    heating_combustible = serpy.IntField()

    # HOTWATER INFOS
    hot_water_is_collective = serpy.BoolField()
    hot_water_has_meters = serpy.BoolField()

    # WATER INFOS
    water_is_collective = serpy.BoolField()
    water_has_meters = serpy.BoolField()

    # DJU CORRECTION
    with_dju_correction = serpy.BoolField()
    ref_dju_correction = serpy.IntField(required=False)


class CoproSerializer(AbstractCoproSerializer):
    climatic_zone = ClimaticZoneRatioSerializer()
    altitude = AltitudeRatioSerializer()


class AbstractGeneralInfosSerializer(AbstractCoproSerializer):
    climatic_zone = serpy.MethodField()
    altitude = serpy.MethodField()

    def get_climatic_zone(self, obj):
        return obj.climatic_zone.code

    def get_altitude(self, obj):
        return obj.altitude.pk


class GeneralInfosSerializer(AbstractGeneralInfosSerializer):
    pk = serpy.IntField()


class DiagnosticSerializer(serpy.Serializer):
    pk = serpy.IntField()
    last_year = serpy.IntField()
    user = UserSimpleSerializer()
    advisor = UserSimpleSerializer()
    comments = serpy.Field(required=False)
    created_at = serpy.Field()
    updated_at = serpy.Field()

    # DATA
    copro = CoproSerializer(required=True, many=False)

    # PARAMS
    params = ParamsSerializer(required=True, many=False)


class SimpleDiagnosticSerializer(serpy.Serializer):
    pk = serpy.IntField(required=False)
    last_year = serpy.IntField()
    user = UserSimpleSerializer()
    advisor = UserSimpleSerializer(required=False)
    comments = serpy.Field(required=False)
    name = serpy.MethodField()
    address = serpy.MethodField()
    updated_at = serpy.MethodField()

    def get_name(self, obj):
        return obj.copro.name

    def get_address(self, obj):
        return obj.copro.address

    def get_updated_at(self, obj):
        return int(time.mktime(obj.updated_at.timetuple())) * 1000

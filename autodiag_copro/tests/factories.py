# -*- coding: utf-8 -*-
import decimal
import random

from factory import SubFactory, fuzzy, lazy_attribute, sequence
from factory.django import DjangoModelFactory

import faker

from accounts.tests.factories import GroupFactory, UserFactory

fake = faker.Factory.create("fr_FR")


class ParamsFactory(DjangoModelFactory):
    """
    Factory for creating MainParams
    """

    class Meta:
        model = "autodiag_copro.MainParams"

    water_cost = decimal.Decimal(random.randrange(10000)) / 100
    avg_living_area = random.randint(40, 200)
    # AVERAGE
    avg_hot_water_conso_ratio = decimal.Decimal(random.randrange(10000)) / 100
    avg_water_conso_ratio = decimal.Decimal(random.randrange(10000)) / 100
    # EFFICIENT
    eff_hot_water_conso_ratio = decimal.Decimal(random.randrange(10000)) / 100
    eff_water_conso_ratio = decimal.Decimal(random.randrange(10000)) / 100

    key = SubFactory(GroupFactory)


class CombustibleParamsFactory(DjangoModelFactory):
    """
    Factory for creating Params
    """

    class Meta:
        model = "autodiag_copro.Params"

    params = SubFactory(ParamsFactory)

    combustible = random.randint(0, 6)

    # AVERAGE
    avg_hot_water_energy_ratio = fuzzy.FuzzyDecimal(1.0, 3.0, 2)
    avg_energy_cost_ratio = fuzzy.FuzzyDecimal(1.0, 3.0, 2)
    # EFFICIENT
    eff_hot_water_energy_ratio = fuzzy.FuzzyDecimal(1.0, 3.0, 2)
    eff_energy_cost_ratio = fuzzy.FuzzyDecimal(1.0, 3.0, 2)


class CoproFactory(DjangoModelFactory):
    """
    Factory for creating a Copro
    """

    class Meta:
        model = "autodiag_copro.Copro"

    name = sequence(lambda n: f"Copropriété {n:03}")
    address = fake.street_address()
    climatic_zone = random.randint(1, 99)
    altitude = random.randint(1, 4)

    # REQUESTER
    contact_last_name = lazy_attribute(lambda o: fake.last_name())
    contact_first_name = lazy_attribute(lambda o: fake.first_name())
    contact_email = lazy_attribute(
        lambda o: f"{o.first_name}.{o.last_name}@{fake.domain_name()}".lower()
        .replace(" ", "-")
        .encode("ascii", "ignore")
        .decode("ascii")
    )
    contact_phone = lazy_attribute(lambda o: fake.phone_number())

    # COPRO DESCRIPTION
    number_of_dwellings = random.randint(0, 11)
    number_of_offices_shops = random.randint(0, 11)
    living_area = random.randint(40, 200)
    number_of_buildings = random.randint(0, 11)
    number_of_floors = random.randint(0, 11)
    syndic_name = lazy_attribute(lambda o: fake.company())
    build_year = random.randint(0, 11)

    # HEATING INFOS
    heating_is_collective = True
    heating_individualisation_mode = random.randint(0, 3)
    heating_individualisation_costs = fuzzy.FuzzyDecimal(1.0, 10.0, 2)
    heating_maintenance_contract_P2 = True
    heating_maintenance_contract_P2_cost = fuzzy.FuzzyDecimal(100.0, 1000.0, 2)
    heating_maintenance_contract_P2_P3 = True
    heating_maintenance_contract_P2_P3_cost = fuzzy.FuzzyDecimal(100.0, 1000.0, 2)
    heating_combustible = random.randint(0, 6)

    # HOTWATER INFOS
    hot_water_is_collective = True
    hot_water_has_meters = True

    # WATER INFOS
    water_is_collective = True
    water_has_meters = True

    # DJU CORRECTION
    with_dju_correction = True
    ref_dju_correction = random.randint(2000, 3001)


class YearlyDataFactory(DjangoModelFactory):
    class Meta:
        ordering = ("-years",)
        verbose_name = "Données annuelles"

    copro = SubFactory(CoproFactory)

    year = random.randint(2013, 2020)
    years = f"{year}-{year + 1}"

    # HEATING
    heating_energy_charges = fuzzy.FuzzyDecimal(1.0, 1000.0, 2)
    energy_consumption = fuzzy.FuzzyDecimal(1.0, 100.0, 2)
    # HOTWATER
    hot_water_energy_charges = fuzzy.FuzzyDecimal(1.0, 1000.0, 2)
    hot_water_consumption_charges = fuzzy.FuzzyDecimal(1.0, 1000.0, 2)
    hot_water_consumption = fuzzy.FuzzyDecimal(1.0, 100.0, 2)
    # WATER
    water_consumption_charges = fuzzy.FuzzyDecimal(1.0, 1000.0, 2)
    water_consumption = fuzzy.FuzzyDecimal(1.0, 100.0, 2)
    # DJU
    dju_correction = random.randint(2000, 3001)


class DiagnosticFactory(DjangoModelFactory):
    """
    Factory for creating Diagnostic
    """

    class Meta:
        model = "autodiag_copro.Diagnostic"

    user = SubFactory(UserFactory)
    # DATA
    copro = SubFactory(CoproFactory)
    yearly_datas = YearlyDataFactory.create_batch(5, years="2013-2014")
    # PARAMS
    main_params = SubFactory(ParamsFactory)
    combustibles_params = SubFactory(CombustibleParamsFactory)

    comments = fake.paragraphs(nb=3, ext_word_list=None)

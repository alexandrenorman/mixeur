from decimal import Decimal

import factory
import factory.fuzzy

from energies.models import (
    BuildingHeatingConsumption,
    Energy,
    EnergyVector,
    ProductionSystem,
)


class EnergyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "energies.Energy"
        django_get_or_create = ("identifier",)

    identifier = factory.fuzzy.FuzzyChoice((k for k, v in Energy.ENERGIE_CHOICES))
    primary_energy_ratio = factory.Faker(
        "pydecimal", min_value=Decimal("0"), max_value=Decimal("3")
    )
    ghg_ratio = factory.Faker(
        "pydecimal", min_value=Decimal("0"), max_value=Decimal("1")
    )
    carbon_tax = factory.Faker("pybool")


class EnergyVectorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "energies.EnergyVector"
        django_get_or_create = ("vector",)

    vector = factory.fuzzy.FuzzyChoice((k for k, v in EnergyVector.VECTOR_CHOICES))
    energy = factory.SubFactory(EnergyFactory)
    buying_unit = "louchettes"
    unit = "bolées"


class BuildingHeatingConsumptionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "energies.BuildingHeatingConsumption"
        django_get_or_create = ("criterion",)

    criterion = factory.fuzzy.FuzzyChoice(
        (k for k, v in BuildingHeatingConsumption.CRITERION_CHOICES)
    )
    heating_consumption = factory.Faker("pyint", min_value=1, max_value=1000)


class ProductionSystemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "energies.ProductionSystem"
        django_get_or_create = ("identifier",)

    identifier = factory.fuzzy.FuzzyChoice(
        (k for k, v in ProductionSystem.SYSTEM_CHOICES)
    )
    energy = factory.SubFactory(EnergyFactory)

    class Params:
        full = factory.Trait(
            identifier=factory.Faker("pystr"),
            is_heating=True,
            is_hot_water=True,
            is_individual=True,
            is_multi_unit=True,
            is_hydro=True,
            efficiency_heating=factory.Faker(
                "pydecimal", min_value=Decimal("0"), max_value=Decimal("1")
            ),
            efficiency_hot_water=factory.Faker(
                "pydecimal", min_value=Decimal("0"), max_value=Decimal("1")
            ),
            enr_ratio_heating=factory.Faker(
                "pydecimal", min_value=Decimal("0"), max_value=Decimal("1")
            ),
            enr_ratio_hot_water=factory.Faker(
                "pydecimal", min_value=Decimal("0"), max_value=Decimal("1")
            ),
            investment_individual_heating=factory.Faker(
                "pyint", min_value=1, max_value=100000
            ),
            investment_individual_hot_water=factory.Faker(
                "pyint", min_value=1, max_value=100000
            ),
            maintenance_individual_heating=factory.Faker(
                "pyint", min_value=1, max_value=100000
            ),
            maintenance_individual_hot_water=factory.Faker(
                "pyint", min_value=1, max_value=100000
            ),
            investment_small_multi_unit_heating=factory.Faker(
                "pyint", min_value=1, max_value=100000
            ),
            investment_small_multi_unit_hot_water=factory.Faker(
                "pyint", min_value=1, max_value=100000
            ),
            maintenance_small_multi_unit_heating=factory.Faker(
                "pyint", min_value=1, max_value=100000
            ),
            maintenance_small_multi_unit_hot_water=factory.Faker(
                "pyint", min_value=1, max_value=100000
            ),
            provisions_small_multi_unit_heating=factory.Faker(
                "pyint", min_value=1, max_value=100000
            ),
            provisions_small_multi_unit_hot_water=factory.Faker(
                "pyint", min_value=1, max_value=100000
            ),
            investment_medium_multi_unit_heating=factory.Faker(
                "pyint", min_value=1, max_value=100000
            ),
            investment_medium_multi_unit_hot_water=factory.Faker(
                "pyint", min_value=1, max_value=100000
            ),
            maintenance_medium_multi_unit_heating=factory.Faker(
                "pyint", min_value=1, max_value=100000
            ),
            maintenance_medium_multi_unit_hot_water=factory.Faker(
                "pyint", min_value=1, max_value=100000
            ),
            provisions_medium_multi_unit_heating=factory.Faker(
                "pyint", min_value=1, max_value=100000
            ),
            provisions_medium_multi_unit_hot_water=factory.Faker(
                "pyint", min_value=1, max_value=100000
            ),
            investment_large_multi_unit_heating=factory.Faker(
                "pyint", min_value=1, max_value=100000
            ),
            investment_large_multi_unit_hot_water=factory.Faker(
                "pyint", min_value=1, max_value=100000
            ),
            maintenance_large_multi_unit_heating=factory.Faker(
                "pyint", min_value=1, max_value=100000
            ),
            maintenance_large_multi_unit_hot_water=factory.Faker(
                "pyint", min_value=1, max_value=100000
            ),
            provisions_large_multi_unit_heating=factory.Faker(
                "pyint", min_value=1, max_value=100000
            ),
            provisions_large_multi_unit_hot_water=factory.Faker(
                "pyint", min_value=1, max_value=100000
            ),
        )

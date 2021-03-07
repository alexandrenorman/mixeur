# -*- coding: utf-8 -*-
import random

from factory import (
    Iterator,
    SubFactory,
    lazy_attribute,
    lazy_attribute_sequence,
)
from factory.django import DjangoModelFactory

import faker

from accounts.tests.factories import (
    AdvisorProfileFactory,
    ClientProfileFactory,
    GroupFactory,
)

from visit_report.models import Housing

fake = faker.Factory.create("fr_FR")


class HousingFactory(DjangoModelFactory):
    class Meta:
        model = "visit_report.Housing"

    user = SubFactory(ClientProfileFactory)
    city = lazy_attribute(lambda o: fake.city())
    postcode = lazy_attribute(lambda o: fake.postcode())
    inseecode = lazy_attribute(lambda o: fake.postcode())
    housing_type = Iterator([x[0] for x in Housing.HOUSING_TYPES])
    ownership = Iterator([x[0] for x in Housing.OWNERSHIP_TYPES])
    area = lazy_attribute(lambda o: random.randint(10, 200))
    occupants_number = lazy_attribute(lambda o: random.randint(1, 10))
    note = lazy_attribute(lambda o: fake.text())
    is_main_address = lazy_attribute(lambda o: fake.boolean())

    @lazy_attribute_sequence
    def address(self, n):
        return f"{fake.street_address()} # {self.postcode} {self.city}"


class ReportFactory(DjangoModelFactory):
    class Meta:
        model = "visit_report.Report"

    housing = SubFactory(HousingFactory)
    advisor = SubFactory(AdvisorProfileFactory)
    group = SubFactory(GroupFactory)
    consumption_information_source = Iterator(
        ["bill", "dpe", "declarative", "estimative", "unavailable"]
    )
    consumption_heating = lazy_attribute(lambda o: random.randint(0, 10000))
    consumption_hot_water = lazy_attribute(lambda o: random.randint(0, 10000))
    consumption_heating_hot_water = lazy_attribute(lambda o: fake.boolean())
    consumption_electricity = lazy_attribute(lambda o: random.randint(0, 100_000))
    dpe = Iterator(["a", "b", "c", "d", "e", "-"])
    consumption_comment = lazy_attribute(lambda o: fake.text())
    house_inventory_comment = lazy_attribute(lambda o: fake.text())
    conclusion_comment = lazy_attribute(lambda o: fake.text())


class FaceFactory(DjangoModelFactory):
    class Meta:
        model = "visit_report.Face"

    report = SubFactory(ReportFactory)
    evaluation = lazy_attribute(lambda o: random.randint(0, 10))
    comment = lazy_attribute(lambda o: fake.text()[0:200])
    insulation_nature = Iterator(["synthetic", "mineral", "biosourced", "undetermined"])
    nature = Iterator(["wall", "floor", "roof", "window"])
    data = lazy_attribute(lambda o: fake.text()[0:1000])


class ScenarioFactory(DjangoModelFactory):
    class Meta:
        model = "visit_report.Scenario"

    report = SubFactory(ReportFactory)
    nature = Iterator(["full", "partial"])
    custom_summary = lazy_attribute(lambda o: fake.text())


class FinancialAidFactory(DjangoModelFactory):
    class Meta:
        model = "visit_report.FinancialAid"

    scenario = SubFactory(ScenarioFactory)
    amount = lazy_attribute(lambda o: random.randint(0, 10))
    selected = lazy_attribute(lambda o: fake.boolean())
    custom_label = lazy_attribute(lambda o: fake.text()[0:50])


class FinancingFactory(DjangoModelFactory):
    class Meta:
        model = "visit_report.Financing"

    scenario = SubFactory(ScenarioFactory)
    amount = lazy_attribute(lambda o: random.randint(0, 10))
    selected = lazy_attribute(lambda o: fake.boolean())


class ScenarioSummaryFactory(DjangoModelFactory):
    class Meta:
        model = "visit_report.ScenarioSummary"

    scenario = SubFactory(ScenarioFactory)


class StepFactory(DjangoModelFactory):
    class Meta:
        model = "visit_report.Step"

    report = SubFactory(ReportFactory)
    category = Iterator(
        ["estimation", "estimation_signature", "work_beginning", "work_end"]
    )
    order = lazy_attribute(lambda o: random.randint(0, 10))
    nature = Iterator(["simple", "info", "contact", "field"])
    data = lazy_attribute(lambda o: fake.text())


class SystemFactory(DjangoModelFactory):
    class Meta:
        model = "visit_report.System"

    report = SubFactory(ReportFactory)
    nature = Iterator(
        [
            "heating_main",
            "emitter",
            "controler",
            "hot_water",
            "heating_extra",
            "ventilation",
            "photovoltaic",
        ]
    )
    data = lazy_attribute(lambda o: fake.text())


class WorkRecommendationFactory(DjangoModelFactory):
    class Meta:
        model = "visit_report.WorkRecommendation"

    report = SubFactory(ReportFactory)
    category = Iterator(["envelope", "system", "other"])
    nature = Iterator(
        [
            "roof_insulation",
            "wall_insulation",
            "floor_insulation",
            "carpentry_replacement",
            "ventilation",
            "heating_production",
            "hot_water_production",
            "heating_control",
            "photovoltaic",
            "eco_gestures",
        ]
    )
    name = lazy_attribute(lambda o: fake.text()[0:50])
    selected = lazy_attribute(lambda o: fake.boolean())
    cost = lazy_attribute(lambda o: random.randint(0, 10))
    comment = lazy_attribute(lambda o: fake.text())
    selected_scenario_secondary = lazy_attribute(lambda o: fake.boolean())
    data = lazy_attribute(lambda o: fake.text())

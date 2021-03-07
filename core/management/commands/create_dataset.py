# -*- coding: utf-8 -*-
import random

from django.core.management.base import BaseCommand
from django.db import transaction

from accounts.tests.factories import GroupFactory, ClientProfileFactory
from visit_report.tests.factories import (
    FaceFactory,
    FinancialAidFactory,
    FinancingFactory,
    HousingFactory,
    ScenarioFactory,
    ScenarioSummaryFactory,
    StepFactory,
    SystemFactory,
    VisitReportFactory,
    WorkRecommendationFactory,
)

from territories.models import Commune
from accounts.models import Group


class Command(BaseCommand):
    """
    """

    help = "Create a dataset from scratch"

    def add_arguments(self, parser):
        parser.add_argument("-g", "--groups", type=int, help="Number of groups")
        parser.add_argument(
            "-a", "--accounts", type=int, help="Number of client accounts"
        )
        parser.add_argument(
            "-b", "--housings", type=int, help="Number of housing per client account"
        )
        parser.add_argument(
            "-r",
            "--visit-report",
            help="Create visit report for each housing",
            action="store_true",
        )

    def handle(self, *args, **options):
        nb_groups = options["groups"]
        nb_accounts = options["accounts"]
        nb_housings = options["housings"]
        nb_visit_reports = options["visit_report"]
        self.stdout.write(
            f"Create {nb_groups} groups and {nb_accounts} accounts with {nb_housings} per account."
        )

        towns_nb = Commune.objects.all().count()
        with transaction.atomic():
            if nb_groups:
                for i in range(nb_groups):
                    GroupFactory()

            if nb_accounts:
                for i in range(nb_accounts):
                    u = ClientProfileFactory()

                    if nb_housings:
                        for j in range(nb_housings):
                            h = HousingFactory(user=u)
                            address = h.address.split("#")[0]
                            town = Commune.objects.all()[
                                random.randint(0, towns_nb - 1)
                            ]
                            # h.address = f"{address} {town.postcode} {town.name}"
                            # h.postcode = town.postcode
                            # BUG no postcode in DB for Communes
                            h.address = f"{address} {town.inseecode} {town.name}"
                            h.postcode = town.inseecode
                            h.inseecode = town.inseecode
                            h.city = town.name
                            h.save()

                            if nb_visit_reports:
                                vr = VisitReportFactory(
                                    housing=h,
                                    group=Group.objects.get_or_create(
                                        name="Structure Test"
                                    )[0],
                                )
                                FaceFactory(report=vr)
                                FaceFactory(report=vr)
                                FaceFactory(report=vr)
                                FaceFactory(report=vr)
                                scenario = ScenarioFactory(report=vr)
                                ScenarioSummaryFactory(scenario=scenario)
                                FinancialAidFactory(scenario=scenario)
                                FinancingFactory(scenario=scenario)
                                scenario = ScenarioFactory(report=vr)
                                ScenarioSummaryFactory(scenario=scenario)
                                FinancialAidFactory(scenario=scenario)
                                FinancingFactory(scenario=scenario)
                                StepFactory(report=vr)
                                StepFactory(report=vr)
                                StepFactory(report=vr)
                                SystemFactory(report=vr)
                                SystemFactory(report=vr)
                                SystemFactory(report=vr)
                                SystemFactory(report=vr)
                                WorkRecommendationFactory(report=vr)

        return

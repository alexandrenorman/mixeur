# -*- coding: utf-8 -*-

# https://django-test-plus.readthedocs.io/en/latest/
from test_plus.test import TestCase

from django.core.exceptions import ValidationError

from .factories import HousingFactory
from accounts.tests.factories import (
    ClientProfileFactory,
    AdvisorProfileFactory,
    ManagerProfileFactory,
    AdministratorProfileFactory,
)

from simple_perms.helpers import AssertPermissions
from visit_report.models import Housing


class HousingTestCase(AssertPermissions, TestCase):
    def setUp(self):
        self.client = ClientProfileFactory()
        self.advisor = AdvisorProfileFactory()
        self.manager = ManagerProfileFactory()
        self.administrator = AdministratorProfileFactory()

        self.housing = HousingFactory(user=self.client)

    def test_no_user_for_housing(self):
        self.housing.user = None
        self.housing.clean()

    def test_client_can_have_housing(self):
        self.housing.user = self.client
        self.housing.clean()

    def test_advisor_cannot_have_housing(self):
        with self.assertRaises(ValidationError) as context:
            self.housing.user = self.advisor
            self.housing.clean()

        self.assertTrue(
            "Un logement ne peut être associé qu'à un profil client."
            in context.exception
        )

    def test_manager_cannot_have_housing(self):
        with self.assertRaises(ValidationError) as context:
            self.housing.user = self.manager
            self.housing.clean()

        self.assertTrue(
            "Un logement ne peut être associé qu'à un profil client."
            in context.exception
        )

    def test_administrator_cannot_have_housing(self):
        with self.assertRaises(ValidationError) as context:
            self.housing.user = self.administrator
            self.housing.clean()

        self.assertTrue(
            "Un logement ne peut être associé qu'à un profil client."
            in context.exception
        )

    def test_only_one_main_address_by_client(self):
        h2 = HousingFactory(user=self.client, is_main_address=True)
        h2.clean()
        self.assertEquals(
            Housing.objects.filter(user=self.client, is_main_address=True).count(), 1
        )
        self.assertEquals(
            Housing.objects.filter(user=self.client, is_main_address=True)[0], h2
        )

    def test_get_main_address_from_user(self):
        h2 = HousingFactory(user=self.client, is_main_address=True)
        h2.clean()
        h2.save()
        self.assertEquals(h2, self.client.main_housing)

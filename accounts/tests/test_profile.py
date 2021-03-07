# -*- coding: utf-8 -*-

from django.core.exceptions import ValidationError

from test_plus.test import TestCase

from .factories import (
    AdminGroupFactory,
    AdministratorProfileFactory,
    AdvisorProfileFactory,
    ClientProfileFactory,
    GroupFactory,
    ManagerProfileFactory,
)


class ProfileTestCase(TestCase):
    def setUp(self):
        self.client = ClientProfileFactory()
        self.advisor = AdvisorProfileFactory()
        self.manager = ManagerProfileFactory()
        self.administrator = AdministratorProfileFactory()
        self.admin_group = AdminGroupFactory()
        self.group = GroupFactory()

    def test_manager_cant_have_normal_group(self):
        self.manager.group = self.group
        with self.assertRaises(ValidationError) as context:
            self.manager.clean()

        self.assertTrue(
            "Un profil « manager » ne peut pas être appartenir à un groupe normal."
            in context.exception
        )

    def test_manager_must_have_admin_group(self):
        self.manager.group = None
        with self.assertRaises(ValidationError) as context:
            self.manager.clean()

        self.assertTrue(
            "Un profil « manager » doit appartenir à un groupe admin."
            in context.exception
        )

    def test_manager_can_have_admin_group(self):
        self.manager.group = self.admin_group
        self.manager.clean()

    def test_client_cant_be_superuser(self):
        self.client.is_superuser = True
        with self.assertRaises(ValidationError) as context:
            self.client.clean()

        self.assertTrue(
            "Un profil « client » ou « professionnel » ne peut pas être superuser."
            in context.exception
        )

    def test_client_cant_have_group(self):
        self.client.group = self.group
        with self.assertRaises(ValidationError) as context:
            self.client.clean()

        self.assertTrue(
            "Un profil « client » ou « professionnel » ne peut pas être affecté à un groupe."
            in context.exception
        )

    def test_advisor_cant_have_admin_group(self):
        self.advisor.group = self.admin_group
        with self.assertRaises(ValidationError) as context:
            self.advisor.clean()

        self.assertTrue(
            "Un profil « conseiller » ne peut pas être affecté à un groupe d'administration."
            in context.exception
        )

    def test_advisor_must_have_a_group(self):
        self.advisor.group = None
        with self.assertRaises(ValidationError) as context:
            self.advisor.clean()

        self.assertTrue(
            "Un profil « conseiller » doit être affecté à un groupe."
            in context.exception
        )

    def test_administrator_cant_have_any_group(self):
        self.administrator.group = self.admin_group
        with self.assertRaises(ValidationError) as context:
            self.administrator.clean()

        self.assertTrue(
            "Un profil « administrateur » ne peut pas être affecté à un groupe."
            in context.exception
        )

        self.administrator.group = self.group
        with self.assertRaises(ValidationError) as context:
            self.administrator.clean()

        self.assertTrue(
            "Un profil « administrateur » ne peut pas être affecté à un groupe."
            in context.exception
        )

    def test_client(self):
        self.assertFalse(self.client.is_contact)
        self.assertTrue(self.client.is_client)
        self.assertFalse(self.client.is_advisor)
        self.assertFalse(self.client.is_manager)
        self.assertFalse(self.client.is_administrator)
        self.assertTrue(self.client.can_login)

    def test_advisor(self):
        self.assertFalse(self.advisor.is_contact)
        self.assertFalse(self.advisor.is_client)
        self.assertTrue(self.advisor.is_advisor)
        self.assertFalse(self.advisor.is_manager)
        self.assertFalse(self.advisor.is_administrator)
        self.assertTrue(self.advisor.can_login)

    def test_manager(self):
        self.assertFalse(self.manager.is_contact)
        self.assertFalse(self.manager.is_client)
        self.assertFalse(self.manager.is_advisor)
        self.assertTrue(self.manager.is_manager)
        self.assertFalse(self.manager.is_administrator)
        self.assertTrue(self.manager.can_login)

    def test_administrator(self):
        self.assertFalse(self.administrator.is_contact)
        self.assertFalse(self.administrator.is_client)
        self.assertFalse(self.administrator.is_advisor)
        self.assertFalse(self.administrator.is_manager)
        self.assertTrue(self.administrator.is_administrator)
        self.assertTrue(self.administrator.can_login)

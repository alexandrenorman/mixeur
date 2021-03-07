# -*- coding: utf-8 -*-

from simple_perms.helpers import AssertPermissions

from test_plus.test import TestCase

from accounts.tests.factories import (
    AdministratorProfileFactory,
    AdvisorProfileFactory,
    ClientProfileFactory,
    ManagerProfileFactory,
)

from .factories import HousingFactory


class HousingPermTestCase(AssertPermissions, TestCase):
    def setUp(self):
        self.client = ClientProfileFactory()
        self.other_client = ClientProfileFactory()
        self.advisor = AdvisorProfileFactory()
        self.manager = ManagerProfileFactory()
        self.administrator = AdministratorProfileFactory()

        self.housing = HousingFactory(user=self.client)
        self.other_housing = HousingFactory(user=self.other_client)

    def test_client_perms(self):
        # fmt: off
        permissions = [
            {'usr': 'client', 'perm': 'visit_report/housing.view', 'args': (self.housing, ),       'result': True},   # NOQA: E501,E241
            {'usr': 'client', 'perm': 'visit_report/housing.view', 'args': (self.other_housing, ), 'result': False},  # NOQA: E501,E241
        ]
        # fmt: on
        self.assertPerms(permissions)

    def test_advisor_perms(self):
        # fmt: off
        permissions = [
            {'usr': 'advisor', 'perm': 'visit_report/housing.view', 'args': (self.housing, ),       'result': True},   # NOQA: E501,E241
            {'usr': 'advisor', 'perm': 'visit_report/housing.view', 'args': (self.other_housing, ), 'result': True},  # NOQA: E501,E241
        ]
        # fmt: on
        self.assertPerms(permissions)

    def test_manager_perms(self):
        # fmt: off
        permissions = [
            {'usr': 'manager', 'perm': 'visit_report/housing.view', 'args': (self.housing, ),       'result': True},   # NOQA: E501,E241
            {'usr': 'manager', 'perm': 'visit_report/housing.view', 'args': (self.other_housing, ), 'result': True},  # NOQA: E501,E241
        ]
        # fmt: on
        self.assertPerms(permissions)

    def test_administrator_perms(self):
        # fmt: off
        permissions = [
            {'usr': 'administrator', 'perm': 'visit_report/housing.view', 'args': (self.housing, ),       'result': True},   # NOQA: E501,E241
            {'usr': 'administrator', 'perm': 'visit_report/housing.view', 'args': (self.other_housing, ), 'result': True},  # NOQA: E501,E241
        ]
        # fmt: on
        self.assertPerms(permissions)

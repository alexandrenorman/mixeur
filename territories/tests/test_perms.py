# -*- coding: utf-8 -*-

# https://django-test-plus.readthedocs.io/en/latest/
from test_plus.test import TestCase

from accounts.tests.factories import (
    ClientProfileFactory,
    AdvisorProfileFactory,
    ManagerProfileFactory,
    AdministratorProfileFactory,
    GroupFactory,
    AdminGroupFactory,
)
from .factories import CommuneFactory

from simple_perms.helpers import AssertPermissions


class CommunePermTestCase(AssertPermissions, TestCase):
    def setUp(self):
        self.client = ClientProfileFactory()

        self.admin_group = AdminGroupFactory(name="admin group")
        self.other_admin_group = AdminGroupFactory(name="other admin group")

        self.group = GroupFactory(admin_group=self.admin_group, name="Group")
        self.other_group = GroupFactory(
            admin_group=self.other_admin_group, name="Other Group"
        )

        self.advisor = AdvisorProfileFactory(group=self.group)
        self.manager = ManagerProfileFactory(group=self.admin_group)
        self.administrator = AdministratorProfileFactory(group=self.group)

        self.other_advisor = AdvisorProfileFactory(group=self.other_group)
        self.other_manager = ManagerProfileFactory(group=self.other_admin_group)
        self.other_administrator = AdministratorProfileFactory(group=self.other_group)

        self.commune_ok_1 = CommuneFactory()
        self.commune_ok_2 = CommuneFactory()
        self.commune_nok = CommuneFactory()

        self.admin_group.territories.add(self.commune_ok_1)
        self.admin_group.territories.add(self.commune_ok_2)

        self.group.territories.add(self.commune_ok_1)

        self.other_admin_group.territories.add(self.commune_nok)

    def test_client_perms(self):
        # fmt: off
        permissions = [
            {'usr': 'client', 'perm': 'commune.may_use',  'args': (self.commune_ok_1, ),  'result': False},  # NOQA: E501,E241
            {'usr': 'client', 'perm': 'commune.may_use',  'args': (self.commune_ok_2, ),  'result': False},  # NOQA: E501,E241
            {'usr': 'client', 'perm': 'commune.may_use',  'args': (self.commune_nok, ),   'result': False},  # NOQA: E501,E241
            {'usr': 'client', 'perm': 'commune.can_use',  'args': (self.commune_ok_1, ),  'result': False},  # NOQA: E501,E241
            {'usr': 'client', 'perm': 'commune.can_use',  'args': (self.commune_ok_2, ),  'result': False},  # NOQA: E501,E241
            {'usr': 'client', 'perm': 'commune.can_use',  'args': (self.commune_nok, ),   'result': False},  # NOQA: E501,E241
        ]
        # fmt: on
        self.assertPerms(permissions)

    def test_advisor_perms(self):
        # fmt: off
        permissions = [
            {'usr': 'advisor', 'perm': 'commune.may_use',  'args': (self.commune_ok_1, ),  'result': True},   # NOQA: E501,E241
            {'usr': 'advisor', 'perm': 'commune.may_use',  'args': (self.commune_ok_2, ),  'result': True},  # NOQA: E501,E241
            {'usr': 'advisor', 'perm': 'commune.may_use',  'args': (self.commune_nok, ),   'result': False},  # NOQA: E501,E241
            {'usr': 'advisor', 'perm': 'commune.can_use',  'args': (self.commune_ok_1, ),  'result': True},   # NOQA: E501,E241
            {'usr': 'advisor', 'perm': 'commune.can_use',  'args': (self.commune_ok_2, ),  'result': False},  # NOQA: E501,E241
            {'usr': 'advisor', 'perm': 'commune.can_use',  'args': (self.commune_nok, ),   'result': False},  # NOQA: E501,E241
        ]
        # fmt: on
        self.assertPerms(permissions)

    def test_manager_perms(self):
        # fmt: off
        permissions = [
            {'usr': 'manager', 'perm': 'commune.may_use',  'args': (self.commune_ok_1, ),  'result': True},   # NOQA: E501,E241
            {'usr': 'manager', 'perm': 'commune.may_use',  'args': (self.commune_ok_2, ),  'result': True},   # NOQA: E501,E241
            {'usr': 'manager', 'perm': 'commune.may_use',  'args': (self.commune_nok, ),   'result': False},  # NOQA: E501,E241
            {'usr': 'manager', 'perm': 'commune.can_use',  'args': (self.commune_ok_1, ),  'result': True},   # NOQA: E501,E241
            {'usr': 'manager', 'perm': 'commune.can_use',  'args': (self.commune_ok_2, ),  'result': True},   # NOQA: E501,E241
            {'usr': 'manager', 'perm': 'commune.can_use',  'args': (self.commune_nok, ),   'result': False},  # NOQA: E501,E241
        ]
        # fmt: on
        self.assertPerms(permissions)

    def test_administrator_perms(self):
        # fmt: off
        permissions = [
            {'usr': 'administrator', 'perm': 'commune.may_use',  'args': (self.commune_ok_1, ),  'result': True},   # NOQA: E501,E241
            {'usr': 'administrator', 'perm': 'commune.may_use',  'args': (self.commune_ok_2, ),  'result': True},   # NOQA: E501,E241
            {'usr': 'administrator', 'perm': 'commune.may_use',  'args': (self.commune_nok, ),   'result': True},   # NOQA: E501,E241
            {'usr': 'administrator', 'perm': 'commune.can_use',  'args': (self.commune_ok_1, ),  'result': True},   # NOQA: E501,E241
            {'usr': 'administrator', 'perm': 'commune.can_use',  'args': (self.commune_ok_2, ),  'result': True},   # NOQA: E501,E241
            {'usr': 'administrator', 'perm': 'commune.can_use',  'args': (self.commune_nok, ),   'result': True},   # NOQA: E501,E241
        ]
        # fmt: on
        self.assertPerms(permissions)

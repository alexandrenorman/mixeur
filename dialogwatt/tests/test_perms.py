# -*- coding: utf-8 -*-
from test_plus.test import TestCase

from accounts.tests.factories import (
    AdvisorProfileFactory,
    ClientProfileFactory,
    GroupFactory,
    AdminGroupFactory,
    ManagerProfileFactory,
    AdministratorProfileFactory,
)

from .factories import AppointmentFactory

from simple_perms.helpers import AssertPermissions


class AppointmentPermTestCase(AssertPermissions, TestCase):
    def setUp(self):
        self.client = ClientProfileFactory()
        self.advisor = AdvisorProfileFactory()

        self.admin_group = AdminGroupFactory()
        self.other_admin_group = AdminGroupFactory()

        self.group = GroupFactory(admin_group=self.admin_group)
        self.other_group = GroupFactory(admin_group=self.other_admin_group)

        self.advisor = AdvisorProfileFactory(group=self.group)
        self.manager = ManagerProfileFactory(group=self.admin_group)
        self.administrator = AdministratorProfileFactory(group=self.group)

        self.other_client = ClientProfileFactory()
        self.other_advisor_in_same_group = AdvisorProfileFactory(group=self.group)
        self.other_advisor_in_other_group = AdvisorProfileFactory(
            group=self.other_group
        )
        self.other_manager = ManagerProfileFactory(group=self.other_admin_group)
        self.other_administrator = AdministratorProfileFactory(group=self.other_group)

        self.appointment = AppointmentFactory(
            client_or_contact=self.client, advisor=self.advisor
        )

    def test_advisor_perms(self):
        # fmt: off
        permissions = [
            {'usr': 'advisor', 'perm': 'dialogwatt/appointment.view',     'args': (self.appointment, ),  'result': True},   # NOQA: E501,E241
            {'usr': 'advisor', 'perm': 'dialogwatt/appointment.change',   'args': (self.appointment, ),  'result': True},   # NOQA: E501,E241
            {'usr': 'advisor', 'perm': 'dialogwatt/appointment.delete',   'args': (self.appointment, ),  'result': True},   # NOQA: E501,E241
        ]
        # fmt: on
        self.assertPerms(permissions)

    def test_client_perms(self):
        # fmt: off
        permissions = [
            {'usr': 'client', 'perm': 'dialogwatt/appointment.view',     'args': (self.appointment, ),  'result': True},   # NOQA: E501,E241
            {'usr': 'client', 'perm': 'dialogwatt/appointment.change',   'args': (self.appointment, ),  'result': True},   # NOQA: E501,E241
            {'usr': 'client', 'perm': 'dialogwatt/appointment.delete',   'args': (self.appointment, ),  'result': True},   # NOQA: E501,E241
        ]
        # fmt: on
        self.assertPerms(permissions)

    def test_other_client_perms(self):
        # fmt: off
        permissions = [
            {'usr': 'other_client', 'perm': 'dialogwatt/appointment.view',     'args': (self.appointment, ),  'result': False},   # NOQA: E501,E241
            {'usr': 'other_client', 'perm': 'dialogwatt/appointment.change',   'args': (self.appointment, ),  'result': False},   # NOQA: E501,E241
            {'usr': 'other_client', 'perm': 'dialogwatt/appointment.delete',   'args': (self.appointment, ),  'result': False},   # NOQA: E501,E241
        ]
        # fmt: on
        self.assertPerms(permissions)

    def test_other_advisor_in_same_group_perms(self):
        # fmt: off
        permissions = [
            {'usr': 'other_advisor_in_same_group', 'perm': 'dialogwatt/appointment.view',     'args': (self.appointment, ),  'result': True},   # NOQA: E501,E241
            {'usr': 'other_advisor_in_same_group', 'perm': 'dialogwatt/appointment.change',   'args': (self.appointment, ),  'result': True},   # NOQA: E501,E241
            {'usr': 'other_advisor_in_same_group', 'perm': 'dialogwatt/appointment.delete',   'args': (self.appointment, ),  'result': True},   # NOQA: E501,E241
        ]
        # fmt: on
        self.assertPerms(permissions)

    def test_other_advisor_in_other_group_perms(self):
        # fmt: off
        permissions = [
            {'usr': 'other_advisor_in_other_group', 'perm': 'dialogwatt/appointment.view',     'args': (self.appointment, ),  'result': False},   # NOQA: E501,E241
            {'usr': 'other_advisor_in_other_group', 'perm': 'dialogwatt/appointment.change',   'args': (self.appointment, ),  'result': False},   # NOQA: E501,E241
            {'usr': 'other_advisor_in_other_group', 'perm': 'dialogwatt/appointment.delete',   'args': (self.appointment, ),  'result': False},   # NOQA: E501,E241
        ]
        # fmt: on
        self.assertPerms(permissions)

    def test_manager_perms(self):
        # fmt: off
        permissions = [
            {'usr': 'manager', 'perm': 'dialogwatt/appointment.view',     'args': (self.appointment, ),  'result': False},   # NOQA: E501,E241
            {'usr': 'manager', 'perm': 'dialogwatt/appointment.change',   'args': (self.appointment, ),  'result': False},   # NOQA: E501,E241
            {'usr': 'manager', 'perm': 'dialogwatt/appointment.delete',   'args': (self.appointment, ),  'result': False},   # NOQA: E501,E241
        ]
        # fmt: on
        self.assertPerms(permissions)

    def test_administrator_perms(self):
        # fmt: off
        permissions = [
            {'usr': 'administrator', 'perm': 'dialogwatt/appointment.view',     'args': (self.appointment, ),  'result': True},   # NOQA: E501,E241
            {'usr': 'administrator', 'perm': 'dialogwatt/appointment.change',   'args': (self.appointment, ),  'result': True},   # NOQA: E501,E241
            {'usr': 'administrator', 'perm': 'dialogwatt/appointment.delete',   'args': (self.appointment, ),  'result': True},   # NOQA: E501,E241
        ]
        # fmt: on
        self.assertPerms(permissions)

# -*- coding: utf-8 -*-

# https://django-test-plus.readthedocs.io/en/latest/
from test_plus.test import TestCase

from django.core.exceptions import ValidationError

from .factories import GroupFactory, AdminGroupFactory


class ProfileTestCase(TestCase):
    def setUp(self):
        self.admin_group = AdminGroupFactory()
        self.other_admin_group = AdminGroupFactory()
        self.group = GroupFactory(admin_group=self.admin_group)
        self.other_group = GroupFactory()

    def test_admin_group_cannot_be_administred_by_admin_group(self):
        self.admin_group.admin_group = self.other_admin_group
        with self.assertRaises(ValidationError) as context:
            self.admin_group.clean()

        self.assertTrue(
            "Un groupe d'administration ne peut pas être administré par un groupe."
            in context.exception
        )

    def test_admin_group_cannot_be_administred_by_group(self):
        self.admin_group.admin_group = self.other_group
        with self.assertRaises(ValidationError) as context:
            self.admin_group.clean()

        self.assertTrue(
            "Un groupe d'administration ne peut pas être administré par un groupe."
            in context.exception
        )

    def test_group_cannot_be_administred_by_group(self):
        self.group.admin_group = self.other_group
        with self.assertRaises(ValidationError) as context:
            self.group.clean()

        self.assertTrue(
            "Un groupe standard doit être administré par un groupe d'administration."
            in context.exception
        )

    def test_group_with_no_admin_group_can_be_saved(self):
        self.other_group.clean()

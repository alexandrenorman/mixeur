# -*- coding: utf-8 -*-

# https://django-test-plus.readthedocs.io/en/latest/
from test_plus.test import TestCase

from django.db.utils import IntegrityError


from accounts.tests.factories import GroupFactory
from .factories import GroupOfNewslettersFactory


class GroupOfNewslettersTestCase(TestCase):
    def setUp(self):
        self.group1 = GroupFactory()
        self.group2 = GroupFactory()

    def test_slug_is_unique_for_group(self):
        gon1 = GroupOfNewslettersFactory(group=self.group1)
        gon1.save()
        with self.assertRaises(IntegrityError) as context:
            gon2 = GroupOfNewslettersFactory(group=self.group1, slug=gon1.slug)
            gon2.save()

        self.assertTrue(
            "duplicate key value violates unique" in context.exception.args[0]
        )

    def test_same_slug_for_different_groups(self):
        gon1 = GroupOfNewslettersFactory(group=self.group1)
        gon1.save()
        gon2 = GroupOfNewslettersFactory(group=self.group2, slug=gon1.slug)
        gon2.save()

        self.assertEqual(gon1.slug, gon2.slug)

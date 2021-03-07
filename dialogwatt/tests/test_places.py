# -*- coding: utf-8 -*-

# https://django-test-plus.readthedocs.io/en/latest/
from test_plus.test import TestCase

from accounts.tests.factories import GroupFactory
from territories.tests.factories import CommuneFactory

from .factories import PlaceFactory

from simple_perms.helpers import AssertPermissions


class PlaceTestCase(AssertPermissions, TestCase):
    def setUp(self):
        self.other_commune = CommuneFactory()
        self.commune_group1_1 = CommuneFactory()
        self.commune_group1_2 = CommuneFactory()
        self.commune_group2_1 = CommuneFactory()
        self.commune_group1_and_2 = CommuneFactory()

        self.group1 = GroupFactory(
            territories=[
                self.commune_group1_1,
                self.commune_group1_2,
                self.commune_group1_and_2,
            ]
        )
        self.group2 = GroupFactory(
            territories=[self.commune_group2_1, self.commune_group1_and_2]
        )

        self.place = PlaceFactory(groups=[self.group1, self.group2])

    def test_territories_from_group(self):
        territories = self.place.territories

        self.assertIn(self.commune_group1_1, territories)
        self.assertIn(self.commune_group1_2, territories)
        self.assertIn(self.commune_group2_1, territories)

        self.assertIn(self.commune_group1_and_2, territories)

        self.assertEquals(
            len([x for x in territories if x == self.commune_group1_and_2]), 1
        )

        self.assertNotIn(self.other_commune, territories)

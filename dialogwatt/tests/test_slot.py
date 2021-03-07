# -*- coding: utf-8 -*-

# https://django-test-plus.readthedocs.io/en/latest/
from test_plus.test import TestCase
from django.core.exceptions import ValidationError

from accounts.tests.factories import AdvisorProfileFactory

from .factories import SlotFactory


class SlotTestCase(TestCase):
    def setUp(self):
        self.slot = SlotFactory()
        self.advisor = AdvisorProfileFactory()

    def test_use_advisor_calendar(self):
        self.slot.use_advisor_calendar = True
        self.slot.number_of_active_advisors = 0
        self.slot.advisors.add(self.advisor)
        self.slot.clean()

    def test_do_not_use_advisor_calendar(self):
        self.slot.use_advisor_calendar = False
        self.slot.number_of_active_advisors = 1
        self.slot.clean()

    def test_use_advisor_calendar_no_number_of_active_advisors(self):
        self.slot.use_advisor_calendar = True
        self.slot.number_of_active_advisors = 1
        with self.assertRaises(ValidationError) as context:
            self.slot.clean()

        self.assertTrue(
            "La gestion des agendas conseillers est incompatible avec le nombre de conseillers simultanés"
            in context.exception
        )

    def test_do_not_use_advisor_calendar_no_use_advisor_calendar(self):
        self.slot.use_advisor_calendar = False
        self.slot.number_of_active_advisors = 0
        with self.assertRaises(ValidationError) as context:
            self.slot.clean()

        self.assertTrue(
            "Le nombre de conseillers simultanés ne peut pas être égal à zéro si la gestion des agendas conseillers est désactivée"  # NOQA: E501
            in context.exception
        )

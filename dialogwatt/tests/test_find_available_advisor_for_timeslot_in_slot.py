# -*- coding: utf-8 -*-

import datetime

from dateutil.relativedelta import relativedelta

from django.utils.timezone import make_aware

from test_plus.test import TestCase

from accounts.tests.factories import AdvisorProfileFactory, GroupFactory

from dialogwatt.helpers import find_available_advisor_for_timeslot_in_slot

from .factories import AppointmentFactory, SlotFactory


class FindAvailableAdvisorForTimeslotInSlotTestCase(TestCase):
    def _times_for_slots_with_appointments(self, chunks):
        return [x["time"] for x in chunks if "time" in x]

    def setUp(self):
        self.group = GroupFactory()

        self.advisor_1 = AdvisorProfileFactory(group=self.group)
        self.advisor_2 = AdvisorProfileFactory(group=self.group)

        self.today = make_aware(
            datetime.datetime.now() + relativedelta(hour=0, minute=0, second=0),
            is_dst=False,
        )

        start_date = self.today + relativedelta(hour=9, minute=0)
        end_date = self.today + relativedelta(hour=18, minute=0)

        self.slot = SlotFactory(
            status="validated",
            group=self.group,
            start_date=start_date,
            end_date=end_date,
            visibility="online",
            use_advisor_calendar=True,
            advisors=[self.advisor_1, self.advisor_2],
            time_between_slots=0,
            deadline=0,
        )
        self.slot_no_advisor_calendar = SlotFactory(
            status="validated",
            group=self.group,
            start_date=start_date,
            end_date=end_date,
            visibility="online",
            use_advisor_calendar=False,
            time_between_slots=0,
            deadline=0,
        )

        self.start = self.today + relativedelta(hour=10, minute=0)
        self.end = self.today + relativedelta(hour=11, minute=0)

    def test_no_existing_appointment(self):
        advisor = find_available_advisor_for_timeslot_in_slot(
            slot=self.slot, start_date=self.start, end_date=self.end
        )

        self.assertIn(advisor, [self.advisor_1, self.advisor_2])

    def test_appointments_before_and_after(self):
        for advisor in [self.advisor_1, self.advisor_2]:
            AppointmentFactory(
                slot=self.slot,
                start_date=self.today + relativedelta(hour=9, minute=0),
                end_date=self.today + relativedelta(hour=9, minute=59),
                advisor=advisor,
            )
            AppointmentFactory(
                slot=self.slot,
                start_date=self.today + relativedelta(hour=11, minute=1),
                end_date=self.today + relativedelta(hour=12, minute=0),
                advisor=advisor,
            )

        advisor = find_available_advisor_for_timeslot_in_slot(
            slot=self.slot, start_date=self.start, end_date=self.end
        )

        self.assertIn(advisor, [self.advisor_1, self.advisor_2])

    def test_appointments_for_advisor_2(self):
        for advisor in [self.advisor_2]:
            AppointmentFactory(
                slot=self.slot,
                start_date=self.today + relativedelta(hour=9, minute=0),
                end_date=self.today + relativedelta(hour=11, minute=0),
                advisor=advisor,
            )

        advisor = find_available_advisor_for_timeslot_in_slot(
            slot=self.slot, start_date=self.start, end_date=self.end
        )

        self.assertEquals(advisor, self.advisor_1)

    def test_no_advisor_available(self):
        for advisor in [self.advisor_1, self.advisor_2]:
            AppointmentFactory(
                slot=self.slot,
                start_date=self.today + relativedelta(hour=9, minute=0),
                end_date=self.today + relativedelta(hour=11, minute=0),
                advisor=advisor,
            )

        with self.assertRaises(ValueError) as context:
            find_available_advisor_for_timeslot_in_slot(
                slot=self.slot, start_date=self.start, end_date=self.end
            )

        self.assertTrue(
            "Aucun conseiller n'est disponible pour ce créneau"
            in context.exception.args
        )

    def test_no_advisor_available_due_to_external_appointment(self):
        for advisor in [self.advisor_1, self.advisor_2]:
            AppointmentFactory(
                slot=None,
                start_date=self.today + relativedelta(hour=9, minute=0),
                end_date=self.today + relativedelta(hour=11, minute=0),
                advisor=advisor,
            )

        with self.assertRaises(ValueError) as context:
            find_available_advisor_for_timeslot_in_slot(
                slot=self.slot, start_date=self.start, end_date=self.end
            )

        self.assertTrue(
            "Aucun conseiller n'est disponible pour ce créneau"
            in context.exception.args
        )

    def test_no_advisor_calendar(self):
        with self.assertRaises(ValueError) as context:
            find_available_advisor_for_timeslot_in_slot(
                slot=self.slot_no_advisor_calendar,
                start_date=self.start,
                end_date=self.end,
            )

        self.assertTrue(
            "Aucun conseiller n'est affectable pour ce créneau"
            in context.exception.args
        )

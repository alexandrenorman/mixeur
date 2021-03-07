# -*- coding: utf-8 -*-
import datetime
import random

from dateutil.relativedelta import relativedelta

from django.db.utils import IntegrityError
from django.utils.timezone import make_aware

import pytz

# https://django-test-plus.readthedocs.io/en/latest/
from test_plus.test import TestCase

from accounts.tests.factories import AdvisorProfileFactory, GroupFactory

from dialogwatt.helpers import FindSlots

from territories.tests.factories import CommuneFactory, DepartementFactory

from .factories import (
    AppointmentFactory,
    CatchmentAreaFactory,
    PlaceFactory,
    ReasonFactory,
    SlotFactory,
)


class FindSlotsTestCase(TestCase):
    def _times_for_slots_with_appointments(self, chunks):
        return [x["time"] for x in chunks if "time" in x]

    def setUp(self):
        departement = DepartementFactory()
        self.communes = []
        commune = None
        for _ in range(40):
            while not commune:
                try:
                    commune = CommuneFactory(departement=departement)
                except IntegrityError:
                    commune = None

            self.communes.append(commune)

        self.group = GroupFactory()

        self.advisor_1 = AdvisorProfileFactory(group=self.group)
        self.advisor_2 = AdvisorProfileFactory(group=self.group)

        self.reasons = [
            ReasonFactory(is_active=True, duration=x * 5, group=self.group)
            for x in range(1, 11)
        ]
        self.places = [PlaceFactory(groups=[self.group]) for x in range(10)]

        self.catchment_area = CatchmentAreaFactory(
            group=self.group,
            territories=[x for x in self.communes[:30] if random.randint(1, 100) > 80],
        )

        self.slots = []
        self.today = make_aware(
            datetime.datetime.now()
            + relativedelta(hour=0)
            + relativedelta(minute=0)
            + relativedelta(second=0),
            is_dst=False,
        )
        for i in range(-10, 30):
            start_date = (
                self.today
                + relativedelta(days=i)
                + relativedelta(hour=9)
                + relativedelta(minute=0)
            )
            end_date = (
                self.today
                + relativedelta(days=i)
                + relativedelta(hour=18)
                + relativedelta(minute=0)
            )
            reasons = [self.reasons[0], self.reasons[1], self.reasons[2]]
            place = random.choice(self.places)
            catchment_area = self.catchment_area

            self.slots.append(
                SlotFactory(
                    status="validated",
                    group=self.group,
                    start_date=start_date,
                    end_date=end_date,
                    visibility="online",
                    reasons=reasons,
                    place=place,
                    catchment_area=catchment_area,
                    use_advisor_calendar=True,
                    advisors=[self.advisor_1],
                    time_between_slots=0,
                    deadline=0,
                )
            )

    def test_available_slots(self):

        fs = FindSlots(
            inseecode=self.communes[0].inseecode,
            start_date=self.today,
            reason=self.reasons[0],
            advisor_visibility=True,
        )
        for i in range(-10, 0):
            self.assertNotIn(
                (self.today + relativedelta(days=i)).date(),
                [x.start_date.date() for x in fs._available_slots()],
            )

        for i in range(0, 10):
            self.assertIn(
                (self.today + relativedelta(days=i)).date(),
                [x.start_date.date() for x in fs._available_slots()],
            )

        for i in range(10, 30):
            self.assertIn(
                (self.today + relativedelta(days=i)).date(),
                [x.start_date.date() for x in fs._available_slots()],
            )

    def test_no_available_slots_for_reason(self):
        fs = FindSlots(
            inseecode=self.communes[0].inseecode,
            start_date=self.today,
            reason=self.reasons[9],
            advisor_visibility=True,
        )
        self.assertEqual(fs._available_slots().count(), 0)

    def test_no_available_slots_for_inseecode(self):
        fs = FindSlots(
            inseecode=self.communes[35].inseecode,
            start_date=self.today,
            reason=self.reasons[9],
            advisor_visibility=True,
        )
        self.assertEqual(fs._available_slots().count(), 0)

    def test_smallest_duration_for_slot(self):
        fs = FindSlots(
            inseecode=self.communes[0].inseecode,
            start_date=self.today,
            reason=self.reasons[0],
            # - nb_of_days=2,
            advisor_visibility=True,
        )
        available_slot = fs._available_slots().first()

        self.assertEqual(fs._smallest_duration_for_slot(available_slot), 5)

    def test_all_chunks_for_slot_with_duration(self):
        fs = FindSlots(
            inseecode=self.communes[0].inseecode,
            start_date=self.today,
            reason=self.reasons[0],
            # - nb_of_days=1,
            advisor_visibility=True,
        )
        start_time = self.today + relativedelta(hour=9) + relativedelta(minute=0)
        end_time = self.today + relativedelta(hour=10) + relativedelta(minute=0)

        chunks = fs._all_chunks_for_slot_with_duration(
            start_time=start_time, end_time=end_time, duration=15
        )

        self.assertEqual(chunks, ["09:00", "09:15", "09:30", "09:45"])

    def test_find_free_time(self):
        fs = FindSlots(
            inseecode=self.communes[0].inseecode,
            start_date=self.today + relativedelta(days=1),
            reason=self.reasons[0],
            # - nb_of_days=1,
            advisor_visibility=True,
        )

        chunks = fs.find_free_time(duration=15)

        self.assertEqual(len(chunks.keys()), 1)

        self.assertEqual(
            list(chunks.keys())[0], self.today.date() + relativedelta(days=1)
        )

        self.maxDiff = None
        self.assertEqual(
            self._times_for_slots_with_appointments(
                chunks[self.today.date() + relativedelta(days=1)][:4]
            ),
            ["09:00", "09:15", "09:30", "09:45"],
        )

    def test_find_free_time_before_appointments(self):
        fs = FindSlots(
            inseecode=self.communes[0].inseecode,
            start_date=self.today + relativedelta(days=1),
            reason=self.reasons[0],
            # - nb_of_days=1,
            advisor_visibility=True,
        )

        slot = fs._available_slots().first()

        AppointmentFactory(
            slot=slot,
            start_date=slot.start_date.astimezone(pytz.timezone("Europe/Paris"))
            + relativedelta(hour=9)
            + relativedelta(minute=30),
            end_date=slot.start_date.astimezone(pytz.timezone("Europe/Paris"))
            + relativedelta(hour=18)
            + relativedelta(minute=15),
            advisor=self.advisor_1,
        )

        chunks = fs.find_free_time(duration=15)

        self.assertEqual(len(chunks.keys()), 1)

        self.assertEqual(
            list(chunks.keys())[0], self.today.date() + relativedelta(days=1)
        )

        self.maxDiff = None
        self.assertEqual(
            self._times_for_slots_with_appointments(
                chunks[self.today.date() + relativedelta(days=1)]
            ),
            ["09:00", "09:15"],
        )

    def test_find_free_time_between_appointments(self):
        fs = FindSlots(
            inseecode=self.communes[0].inseecode,
            start_date=self.today + relativedelta(days=1),
            reason=self.reasons[0],
            # - nb_of_days=1,
            advisor_visibility=True,
        )

        slot = fs._available_slots().first()

        AppointmentFactory(
            slot=slot,
            start_date=slot.start_date.astimezone(pytz.timezone("Europe/Paris"))
            + relativedelta(hour=8)
            + relativedelta(minute=30),
            end_date=slot.start_date.astimezone(pytz.timezone("Europe/Paris"))
            + relativedelta(hour=10)
            + relativedelta(minute=15),
            advisor=self.advisor_1,
        )

        AppointmentFactory(
            slot=slot,
            start_date=slot.start_date.astimezone(pytz.timezone("Europe/Paris"))
            + relativedelta(hour=10)
            + relativedelta(minute=30),
            end_date=slot.start_date.astimezone(pytz.timezone("Europe/Paris"))
            + relativedelta(hour=18)
            + relativedelta(minute=15),
            advisor=self.advisor_1,
        )

        chunks = fs.find_free_time(duration=15)

        self.assertEqual(len(chunks.keys()), 1)

        self.assertEqual(
            list(chunks.keys())[0], self.today.date() + relativedelta(days=1)
        )

        self.maxDiff = None
        self.assertEqual(
            self._times_for_slots_with_appointments(
                chunks[self.today.date() + relativedelta(days=1)]
            ),
            ["10:15"],
        )

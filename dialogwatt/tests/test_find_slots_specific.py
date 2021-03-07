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


class FindSlotsSpecificTestCase(TestCase):
    def _times_for_slots_with_appointments(self, chunks):
        return [x["time"] for x in chunks if "time" in x]

    def _create_appointments_from_timetable(self, slot, timetable):
        for advisor in timetable.keys():
            for (start_hour, start_minute), (end_hour, end_minute) in timetable[
                advisor
            ]:
                AppointmentFactory(
                    slot=slot,
                    start_date=slot.start_date.astimezone(pytz.timezone("Europe/Paris"))
                    + relativedelta(hour=start_hour)
                    + relativedelta(minute=start_minute),
                    end_date=slot.start_date
                    + relativedelta(hour=end_hour)
                    + relativedelta(minute=end_minute),
                    advisor=advisor,
                )

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

    def test_find_from_place(self):
        start_date = self.today + relativedelta(hour=8) + relativedelta(minute=0)
        end_date = self.today + relativedelta(hour=17) + relativedelta(minute=0)
        reasons = [self.reasons[0], self.reasons[1], self.reasons[2]]
        place = random.choice(self.places)
        catchment_area = self.catchment_area

        slot = SlotFactory(
            status="validated",
            group=self.group,
            start_date=start_date,
            end_date=end_date,
            visibility="online",
            reasons=reasons,
            place=place,
            catchment_area=catchment_area,
            use_advisor_calendar=True,
            advisors=[self.advisor_1, self.advisor_2],
            time_between_slots=10,
            deadline=0,
        )

        appointments_timetable = {
            self.advisor_1: [((9, 0), (10, 0)), ((12, 0), (14, 0))],
            self.advisor_2: [((8, 0), (10, 0)), ((11, 0), (13, 0)), ((15, 0), (17, 0))],
        }

        self._create_appointments_from_timetable(slot, appointments_timetable)

        fs = FindSlots(
            place=place,
            start_date=self.today,
            reason=self.reasons[0],
            # - nb_of_days=1,
            advisor_visibility=True,
        )

        chunks = fs.find_free_time(duration=30)

        self.assertEqual(len(chunks.keys()), 1)
        self.assertEqual(list(chunks.keys()), [self.today.date()])

        self.maxDiff = None
        self.assertEqual(
            self._times_for_slots_with_appointments(chunks[self.today.date()]),
            [
                "08:00",
                "10:10",
                "10:50",
                "13:10",
                "13:50",
                "14:30",
                "15:10",
                "15:50",
                "16:30",
            ],
        )

    def test_multiple_advisors(self):
        start_date = self.today + relativedelta(hour=8) + relativedelta(minute=0)
        end_date = self.today + relativedelta(hour=17) + relativedelta(minute=0)
        reasons = [self.reasons[0], self.reasons[1], self.reasons[2]]
        place = random.choice(self.places)
        catchment_area = self.catchment_area

        slot = SlotFactory(
            status="validated",
            group=self.group,
            start_date=start_date,
            end_date=end_date,
            visibility="online",
            reasons=reasons,
            place=place,
            catchment_area=catchment_area,
            use_advisor_calendar=True,
            advisors=[self.advisor_1, self.advisor_2],
            time_between_slots=10,
            deadline=0,
        )

        appointments_timetable = {
            self.advisor_1: [((9, 0), (10, 0)), ((12, 0), (14, 0))],
            self.advisor_2: [((8, 0), (10, 0)), ((11, 0), (13, 0)), ((15, 0), (17, 0))],
        }

        self._create_appointments_from_timetable(slot, appointments_timetable)

        fs = FindSlots(
            inseecode=self.communes[0].inseecode,
            start_date=self.today,
            reason=self.reasons[0],
            # - nb_of_days=1,
            advisor_visibility=True,
        )

        chunks = fs.find_free_time(duration=30)

        self.assertEqual(len(chunks.keys()), 1)
        self.assertEqual(list(chunks.keys()), [self.today.date()])

        self.maxDiff = None
        self.assertEqual(
            self._times_for_slots_with_appointments(chunks[self.today.date()]),
            [
                "08:00",
                "10:10",
                "10:50",
                "13:10",
                "13:50",
                "14:30",
                "15:10",
                "15:50",
                "16:30",
            ],
        )

    def test_time_between_slots(self):
        start_date = self.today + relativedelta(hour=9) + relativedelta(minute=0)
        end_date = self.today + relativedelta(hour=18) + relativedelta(minute=0)
        reasons = [self.reasons[0], self.reasons[1], self.reasons[2]]
        place = random.choice(self.places)
        catchment_area = self.catchment_area

        slot = SlotFactory(
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
            time_between_slots=10,
            deadline=0,
        )

        appointments_timetable = {
            self.advisor_1: [((8, 30), (10, 15)), ((12, 30), (18, 15))]
        }

        self._create_appointments_from_timetable(slot, appointments_timetable)

        fs = FindSlots(
            inseecode=self.communes[0].inseecode,
            start_date=self.today,
            reason=self.reasons[0],
            # - nb_of_days=1,
            advisor_visibility=True,
        )

        chunks = fs.find_free_time(duration=30)

        self.assertEqual(len(chunks.keys()), 1)

        self.assertEqual(list(chunks.keys()), [self.today.date()])

        self.maxDiff = None
        self.assertEqual(
            self._times_for_slots_with_appointments(chunks[self.today.date()]),
            ["10:25", "11:05", "11:45"],
        )

    def test_time_between_slots_new_version(self):
        start_date = self.today + relativedelta(hour=8) + relativedelta(minute=0)
        end_date = self.today + relativedelta(hour=17) + relativedelta(minute=0)
        reasons = [self.reasons[0], self.reasons[1], self.reasons[2]]
        place = random.choice(self.places)
        catchment_area = self.catchment_area

        slot = SlotFactory(
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
            time_between_slots=10,
            deadline=0,
        )

        appointments_timetable = {
            self.advisor_1: [((11, 0), (12, 0)), ((14, 0), (17, 0))]
        }

        self._create_appointments_from_timetable(slot, appointments_timetable)

        fs = FindSlots(
            inseecode=self.communes[0].inseecode,
            start_date=self.today,
            reason=self.reasons[0],
            # - nb_of_days=1,
            advisor_visibility=True,
        )

        chunks = fs.find_free_time(duration=30)

        self.assertEqual(len(chunks.keys()), 1)

        self.assertEqual(list(chunks.keys()), [self.today.date()])

        self.maxDiff = None
        self.assertEqual(
            self._times_for_slots_with_appointments(chunks[self.today.date()]),
            ["08:00", "08:40", "09:20", "10:00", "12:10", "12:50"],
        )

    def test_no_use_advisor_calendar_with_multiple(self):
        start_date = self.today + relativedelta(hour=8) + relativedelta(minute=0)
        end_date = self.today + relativedelta(hour=17) + relativedelta(minute=0)
        reasons = [self.reasons[0], self.reasons[1], self.reasons[2]]
        place = random.choice(self.places)
        catchment_area = self.catchment_area

        slot = SlotFactory(
            status="validated",
            group=self.group,
            start_date=start_date,
            end_date=end_date,
            visibility="online",
            reasons=reasons,
            place=place,
            catchment_area=catchment_area,
            use_advisor_calendar=False,
            number_of_active_advisors=2,
            time_between_slots=10,
            deadline=0,
        )

        appointments_timetable = {
            None: [
                ((9, 0), (10, 0)),
                ((12, 0), (14, 0)),
                ((8, 0), (10, 0)),
                ((11, 0), (13, 0)),
                ((15, 0), (17, 0)),
            ]
        }

        self._create_appointments_from_timetable(slot, appointments_timetable)

        fs = FindSlots(
            inseecode=self.communes[0].inseecode,
            start_date=self.today,
            reason=self.reasons[0],
            # - nb_of_days=1,
            advisor_visibility=True,
        )

        chunks = fs.find_free_time(duration=30)

        self.assertEqual(len(chunks.keys()), 1)
        self.assertEqual(list(chunks.keys()), [self.today.date()])

        self.maxDiff = None
        self.assertEqual(
            self._times_for_slots_with_appointments(chunks[self.today.date()]),
            [
                "08:00",
                "10:10",
                "10:50",
                "13:10",
                "13:50",
                "14:30",
                "15:10",
                "15:50",
                "16:30",
            ],
        )

    def test_deadline(self):
        start_date = self.today + relativedelta(hour=8) + relativedelta(minute=0)
        end_date = self.today + relativedelta(hour=17) + relativedelta(minute=0)

        reasons = [self.reasons[0], self.reasons[1], self.reasons[2]]
        place = random.choice(self.places)
        catchment_area = self.catchment_area

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
            time_between_slots=10,
            deadline=24,
        )

        start_date2 = (
            self.today
            + relativedelta(days=2)
            + relativedelta(hour=8)
            + relativedelta(minute=0)
        )
        end_date2 = (
            self.today
            + relativedelta(days=2)
            + relativedelta(hour=17)
            + relativedelta(minute=0)
        )
        slot2 = SlotFactory(
            status="validated",
            group=self.group,
            start_date=start_date2,
            end_date=end_date2,
            visibility="online",
            reasons=reasons,
            place=place,
            catchment_area=catchment_area,
            use_advisor_calendar=True,
            advisors=[self.advisor_1],
            time_between_slots=10,
            deadline=24,
        )

        fs = FindSlots(
            inseecode=self.communes[0].inseecode,
            start_date=self.today,
            reason=self.reasons[0],
            # - nb_of_days=3,
            advisor_visibility=True,
        )

        chunks = fs.find_free_time(duration=30)
        self.assertEqual(len(chunks.keys()), 1)
        self.assertEqual(list(chunks.keys()), [slot2.start_date.date()])

    def test_multiple_advisors_filtering_one(self):
        start_date = self.today + relativedelta(hour=8) + relativedelta(minute=0)
        end_date = self.today + relativedelta(hour=17) + relativedelta(minute=0)
        reasons = [self.reasons[0], self.reasons[1], self.reasons[2]]
        place = random.choice(self.places)
        catchment_area = self.catchment_area

        slot = SlotFactory(
            status="validated",
            group=self.group,
            start_date=start_date,
            end_date=end_date,
            visibility="online",
            reasons=reasons,
            place=place,
            catchment_area=catchment_area,
            use_advisor_calendar=True,
            advisors=[self.advisor_1, self.advisor_2],
            time_between_slots=10,
            deadline=0,
        )

        appointments_timetable = {
            self.advisor_1: [((9, 0), (10, 0)), ((12, 0), (14, 0))],
            self.advisor_2: [((8, 0), (10, 0)), ((11, 0), (13, 0)), ((15, 0), (17, 0))],
        }

        self._create_appointments_from_timetable(slot, appointments_timetable)

        fs = FindSlots(
            inseecode=self.communes[0].inseecode,
            start_date=self.today,
            reason=self.reasons[0],
            # - nb_of_days=1,
            advisor_visibility=True,
        )

        chunks = fs.find_free_time(duration=30, filter_advisors=[self.advisor_1])

        self.assertEqual(len(chunks.keys()), 1)
        self.assertEqual(list(chunks.keys()), [self.today.date()])

        self.maxDiff = None
        self.assertEqual(
            self._times_for_slots_with_appointments(chunks[self.today.date()]),
            ["08:00", "10:10", "10:50", "14:10", "14:50", "15:30", "16:10"],
        )

    def test_find_multiple_slots_on_same_day(self):
        start_date = (
            self.today
            + relativedelta(days=1)
            + relativedelta(hour=8)
            + relativedelta(minute=0)
        )
        end_date = (
            self.today
            + relativedelta(days=1)
            + relativedelta(hour=12)
            + relativedelta(minute=0)
        )

        reasons = [self.reasons[0], self.reasons[1], self.reasons[2]]
        place = random.choice(self.places)
        catchment_area = self.catchment_area

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
            time_between_slots=10,
        )

        start_date2 = start_date + relativedelta(hour=14) + relativedelta(minute=0)
        end_date2 = end_date + relativedelta(hour=17) + relativedelta(minute=0)

        SlotFactory(
            status="validated",
            group=self.group,
            start_date=start_date2,
            end_date=end_date2,
            visibility="online",
            reasons=reasons,
            place=place,
            catchment_area=catchment_area,
            use_advisor_calendar=True,
            advisors=[self.advisor_1],
            time_between_slots=10,
        )

        fs = FindSlots(
            inseecode=self.communes[0].inseecode,
            start_date=self.today,
            reason=self.reasons[0],
            # - nb_of_days=3,
            advisor_visibility=True,
        )

        chunks = fs.find_free_time(duration=60)

        self.assertEqual(len(chunks.keys()), 1)
        self.assertEqual(list(chunks.keys()), [start_date.date()])

        self.assertEqual(len(chunks[start_date.date()]), 5)

        self.assertEqual(
            self._times_for_slots_with_appointments(chunks[start_date.date()]),
            ["08:00", "09:10", "10:20", "14:00", "15:10"],
        )

# -*- coding: utf-8 -*-

import datetime

from dateutil.relativedelta import relativedelta

from django.utils.timezone import make_aware

import pytz

from test_plus.test import TestCase

from accounts.tests.factories import (
    AdvisorProfileFactory,
    ClientProfileFactory,
    GroupFactory,
)

from dialogwatt.forms import AppointmentForm
from dialogwatt.models import Appointment

from fac.tests.factories import ContactFactory

from .factories import (
    AppointmentFactory,
    CatchmentAreaFactory,
    PlaceFactory,
    ReasonFactory,
    SlotFactory,
)


class AppointmentTestCase(TestCase):
    def setUp(self):
        self.client = ClientProfileFactory()
        self.contact = ContactFactory()
        self.group = GroupFactory()
        self.advisor = AdvisorProfileFactory(group=self.group)

        self.reason = ReasonFactory(is_active=True, duration=60, group=self.group)
        self.place = PlaceFactory(groups=[self.group])

        self.catchment_area = CatchmentAreaFactory(group=self.group)

        self.today = make_aware(
            datetime.datetime.now()
            + relativedelta(hour=0)
            + relativedelta(minute=0)
            + relativedelta(second=0),
            is_dst=False,
        )
        start_date = self.today + relativedelta(hour=0) + relativedelta(minute=0)
        end_date = self.today + relativedelta(hour=7) + relativedelta(minute=0)

        self.slot = SlotFactory(
            status="validated",
            group=self.group,
            start_date=start_date,
            end_date=end_date,
            visibility="online",
            reasons=[self.reason],
            place=self.place,
            catchment_area=self.catchment_area,
            use_advisor_calendar=True,
            advisors=[self.advisor],
            time_between_slots=0,
            deadline=0,
        )

    def test_timezone_between_days(self):
        start_date = (
            self.slot.start_date.astimezone(pytz.timezone("Europe/Paris"))
            + relativedelta(hour=9)
            + relativedelta(minute=0)
        )
        end_date = start_date + relativedelta(minutes=120)

        appointment = AppointmentFactory(
            start_date=start_date,
            end_date=end_date,
            advisor=self.advisor,
            slot=self.slot,
            reason=self.reason,
        )

        data = {
            "start_date": (start_date + relativedelta(hour=10)).isoformat(),
            "end_date": (
                start_date + relativedelta(hour=10) + relativedelta(minutes=120)
            ).isoformat(),
            "subject": appointment.subject,
            "reason": self.reason.pk,
            "advisor": self.advisor.pk,
            "slot": self.slot.pk,
            "group": self.slot.group.pk,
        }

        form = AppointmentForm(data, instance=appointment)
        result = form.is_valid()
        self.assertEquals(form.errors, {})
        self.assertTrue(result)

    def test_client_can_update_unassigned_waiting_appointment(self):
        appointment = AppointmentFactory(
            advisor=self.advisor,
            slot=self.slot,
            reason=self.reason,
            status=Appointment.WAITING,
            client_or_contact=None,
        )
        self.assertTrue(
            self.client.has_perm("dialogwatt/appointment.change_waiting", appointment)
        )

    def test_client_cannot_update_assigned_waiting_appointment(self):
        appointment = AppointmentFactory(
            advisor=self.advisor,
            slot=self.slot,
            reason=self.reason,
            status=Appointment.WAITING,
            client_or_contact=self.contact,
        )
        self.assertFalse(
            self.client.has_perm("dialogwatt/appointment.change_waiting", appointment)
        )

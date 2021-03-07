# -*- coding: utf-8 -*-

# https://django-test-plus.readthedocs.io/en/latest/

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

from dialogwatt.forms import AppointmentBookingForAdvisorForm

from fac.tests.factories import ContactFactory

from .factories import (
    AppointmentFactory,
    CatchmentAreaFactory,
    PlaceFactory,
    ReasonFactory,
    SlotFactory,
)


class AppointmentBookingForAdvisorTestCase(TestCase):
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
        start_date = self.today + relativedelta(hour=9) + relativedelta(minute=0)
        end_date = self.today + relativedelta(hour=18) + relativedelta(minute=0)

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

    def test_form_no_client_no_contact(self):
        data = {
            "reason": self.reason.pk,
            "advisor": self.advisor.pk,
            "slot": self.slot.pk,
            "contact": None,
            "client": None,
            "time": "10:00",
        }

        form = AppointmentBookingForAdvisorForm(data)

        self.assertFalse(form.is_valid())
        self.assertIn("__all__", form.errors)
        self.assertEqual(
            form.errors["__all__"], ["Vous devez sélectionner un client ou un contact"]
        )

    def test_form_client_and_contact(self):
        data = {
            "reason": self.reason.pk,
            "advisor": self.advisor.pk,
            "slot": self.slot.pk,
            "contact": self.contact.pk,
            "client": self.client.pk,
            "time": "10:00",
        }

        form = AppointmentBookingForAdvisorForm(data)

        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["__all__"],
            ["Vous ne pouvez pas sélectionner un client et un contact"],
        )

    def test_form_time_before_slot(self):
        data = {
            "reason": self.reason.pk,
            "advisor": self.advisor.pk,
            "slot": self.slot.pk,
            "contact": None,
            "client": self.client.pk,
            "time": "07:00",
        }

        form = AppointmentBookingForAdvisorForm(data)

        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["__all__"], ["L'horaire est hors du créneau"])

    def test_form_time_after_slot(self):
        data = {
            "reason": self.reason.pk,
            "advisor": self.advisor.pk,
            "slot": self.slot.pk,
            "contact": None,
            "client": self.client.pk,
            "time": "17:30",
        }

        form = AppointmentBookingForAdvisorForm(data)

        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["__all__"], ["L'horaire est hors du créneau"])

    def test_form_ok(self):
        data = {
            "reason": self.reason.pk,
            "advisor": self.advisor.pk,
            "slot": self.slot.pk,
            "contact": None,
            "client": self.client.pk,
            "time": "14:30",
        }

        form = AppointmentBookingForAdvisorForm(data)
        self.assertTrue(form.is_valid())

    def test_form_slot_not_free(self):
        data = {
            "reason": self.reason.pk,
            "advisor": self.advisor.pk,
            "slot": self.slot.pk,
            "contact": None,
            "client": self.client.pk,
            "time": "09:00",
        }

        start_date = (
            self.slot.start_date.astimezone(pytz.timezone("Europe/Paris"))
            + relativedelta(hour=9)
            + relativedelta(minute=0)
        )
        end_date = start_date + relativedelta(minutes=120)

        AppointmentFactory(
            start_date=start_date,
            end_date=end_date,
            advisor=self.advisor,
            client_or_contact=self.contact,
            place=self.slot.place,
            slot=self.slot,
            reason=self.reason,
        )

        form = AppointmentBookingForAdvisorForm(data)

        # Will fail until django/dialogwatt/forms/appointment_booking_form.py
        # TODO Check that slot is still available
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["__all__"], ["Le créneau est déjà pris"])

# -*- coding: utf-8 -*-

# https://django-test-plus.readthedocs.io/en/latest/
from test_plus.test import TestCase

from .factories import FacContactForDialogwattFactory


class FacContactForDialogwattTestCase(TestCase):
    def test_allow_to_use_phone_number_to_send_reminder_no_phone(self):
        contact = FacContactForDialogwattFactory(mobile_phone=None)
        self.assertFalse(contact.allow_to_use_phone_number_to_send_reminder)

    def test_allow_to_use_phone_number_to_send_reminder_with_phone(self):
        contact = FacContactForDialogwattFactory()
        self.assertTrue(contact.allow_to_use_phone_number_to_send_reminder)

    # email is mandatory
    # def test_allow_to_use_email_to_send_reminder_no_mail(self):
    #     contact = FacContactForDialogwattFactory(email=None)
    #     self.assertFalse(
    #         contact.allow_to_use_email_to_send_reminder
    #     )

    def test_allow_to_use_email_to_send_reminder_with_mail(self):
        contact = FacContactForDialogwattFactory()
        self.assertTrue(contact.allow_to_use_email_to_send_reminder)

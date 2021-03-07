# -*- coding: utf-8 -*-
from django.test import TestCase

from .factories import RgpdConsentFactory, ClientProfileFactory


class RgpdConsentTestCase(TestCase):
    def setUp(self):
        self.client = ClientProfileFactory()
        self.rgpd_consent = RgpdConsentFactory(
            user=self.client,
            allow_to_keep_data=True,
            allow_to_use_email_to_send_reminder=True,
            allow_to_use_phone_number_to_send_reminder=True,
            allow_to_share_my_information_with_my_advisor=True,
            allow_to_share_my_information_with_partners=True,
        )

    def test_get_last_rgpd_consent(self):
        rgpd_consent_2 = RgpdConsentFactory(user=self.client)
        self.assertEqual(self.client.last_rgpd_consent, rgpd_consent_2)

    def test_default_values(self):
        self.assertTrue(self.rgpd_consent.allow_to_keep_data)
        self.assertTrue(self.rgpd_consent.allow_to_use_email_to_send_reminder)
        self.assertTrue(self.rgpd_consent.allow_to_use_phone_number_to_send_reminder)
        self.assertTrue(self.rgpd_consent.allow_to_share_my_information_with_my_advisor)
        self.assertTrue(self.rgpd_consent.allow_to_share_my_information_with_partners)

    def test_values_from_user(self):
        rgpd_consent = RgpdConsentFactory(
            user=self.client,
            allow_to_keep_data=True,
            allow_to_use_email_to_send_reminder=False,
            allow_to_use_phone_number_to_send_reminder=False,
            allow_to_share_my_information_with_my_advisor=False,
            allow_to_share_my_information_with_partners=False,
        )

        self.assertEqual(self.client.last_rgpd_consent, rgpd_consent)

        self.assertFalse(self.client.allow_to_use_email_to_send_reminder)
        self.assertFalse(self.client.allow_to_use_phone_number_to_send_reminder)
        self.assertFalse(self.client.allow_to_share_my_information_with_my_advisor)
        self.assertFalse(self.client.allow_to_share_my_information_with_partners)

# -*- coding: utf-8 -*-

from django.core.exceptions import ValidationError

from test_plus.test import TestCase

from messaging.tests.factories import SmsAccountAsTwilioFactory


class SmsAccountTwilioTestCase(TestCase):
    def test_required_fields_for_twilio(self):
        sms_empty_fields = SmsAccountAsTwilioFactory()
        sms_empty_fields.twilio_account = None

        with self.assertRaises(ValidationError) as context:
            sms_empty_fields.full_clean()

        self.assertTrue(
            "Pour un compte de type Twilio, vous devez spécifier le compte, le token et le numéro de téléphone"
            in context.exception.args[0]["__all__"][0].args
        )

        sms_empty_fields = SmsAccountAsTwilioFactory()
        sms_empty_fields.twilio_token = None

        with self.assertRaises(ValidationError) as context:
            sms_empty_fields.full_clean()

        self.assertTrue(
            "Pour un compte de type Twilio, vous devez spécifier le compte, le token et le numéro de téléphone"
            in context.exception.args[0]["__all__"][0].args
        )

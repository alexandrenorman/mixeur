# -*- coding: utf-8 -*-

from django.core.exceptions import ValidationError

# https://django-test-plus.readthedocs.io/en/latest/
from test_plus.test import TestCase

from messaging.tests.factories import SmsAccountAsOvhFactory


class SmsAccountTestCase(TestCase):
    def test_required_fields_for_ovh(self):
        sms_empty_fields = SmsAccountAsOvhFactory()
        sms_empty_fields.ovh_account = None

        with self.assertRaises(ValidationError) as context:
            sms_empty_fields.full_clean()

        self.assertTrue(
            "Pour un compte de type OVH, vous devez spécifier le compte, l'identifiant, le mot de passe et l'identifiant d'expedition"  # NOQA: E501
            in context.exception.args[0]["__all__"][0].args
        )

        sms_empty_fields = SmsAccountAsOvhFactory()
        sms_empty_fields.ovh_login = None

        with self.assertRaises(ValidationError) as context:
            sms_empty_fields.full_clean()

        self.assertTrue(
            "Pour un compte de type OVH, vous devez spécifier le compte, l'identifiant, le mot de passe et l'identifiant d'expedition"  # NOQA: E501
            in context.exception.args[0]["__all__"][0].args
        )

        sms_empty_fields = SmsAccountAsOvhFactory()
        sms_empty_fields.ovh_password = None

        with self.assertRaises(ValidationError) as context:
            sms_empty_fields.full_clean()

        self.assertTrue(
            "Pour un compte de type OVH, vous devez spécifier le compte, l'identifiant, le mot de passe et l'identifiant d'expedition"  # NOQA: E501
            in context.exception.args[0]["__all__"][0].args
        )

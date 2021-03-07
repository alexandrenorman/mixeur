# -*- coding: utf-8 -*-
import datetime

from dateutil.relativedelta import relativedelta

from django.utils.timezone import make_aware

# https://django-test-plus.readthedocs.io/en/latest/
from test_plus.test import TestCase

from accounts.tests.factories import AdvisorProfileFactory, GroupFactory

from dialogwatt.tests.factories import ExchangeFactory

from messaging.tests.factories import SmsAccountFactory


class SmsAccountTestCase(TestCase):
    def setUp(self):
        self.group = GroupFactory()
        self.advisor = AdvisorProfileFactory(group=self.group)
        self.sms_account = SmsAccountFactory(group=self.group, monthly_limit=10)
        return

    def _create_sms_exchanges(self, count, date=None):
        date = (
            date
            if date is not None
            else make_aware(datetime.datetime.now(), is_dst=False)
        )
        for _ in range(count):
            ExchangeFactory(
                group=self.group,
                from_account=self.advisor,
                message_type="sms",
                has_been_sent_on=date,
            )

    def test_can_send_sms(self):
        self.assertTrue(self.sms_account.can_send_sms)

        self._create_sms_exchanges(self.sms_account.monthly_limit)
        self.assertTrue(self.sms_account.can_send_sms)

        self._create_sms_exchanges(1)
        self.assertFalse(self.sms_account.can_send_sms)

    def test_monthly_sent_for_current_month(self):
        self._create_sms_exchanges(15)
        self.assertEqual(self.sms_account.monthly_sent, 15)

    def test_monthly_sent_for_another_month(self):
        date = make_aware(datetime.datetime.now(), is_dst=False) + relativedelta(
            months=-1
        )
        self._create_sms_exchanges(25, date)
        self.assertEqual(self.sms_account.monthly_sent, 0)
        self.assertEqual(self.sms_account.monthly_sent_on_month(date), 25)

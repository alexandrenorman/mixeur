# -*- coding: utf-8 -*-

import datetime
from unittest import mock

from django.contrib.contenttypes.models import ContentType
from django.utils.timezone import make_aware

from test_plus.test import TestCase


from accounts.tests.factories import (
    AdvisorProfileFactory,
    ClientProfileFactory,
    GroupFactory,
    RgpdConsentFactory,
)

from dialogwatt.helpers import NotificationManager
from dialogwatt.models import NotificationRequested

from messaging.tests.factories import SmsAccountAsOvhFactory, SmtpAccountAsSmtpFactory

from .factories import (
    AppointmentFactory,
    NotificationFactory,
    PlaceFactory,
    ReasonFactory,
)


class NotificationManagerTestCase(TestCase):
    def setUp(self):
        self.group = GroupFactory(name="Hespul", phone="0327478090")

        self.sms_account = SmsAccountAsOvhFactory(group=self.group)
        self.smtp_account = SmtpAccountAsSmtpFactory(group=self.group)

        self.advisor1 = AdvisorProfileFactory(
            group=self.group, first_name="Conseiller", last_name="Test"
        )
        self.advisor2 = AdvisorProfileFactory(group=self.group)
        self.advisor3 = AdvisorProfileFactory(group=self.group)

        self.place = PlaceFactory(
            name="Accueil", phone="0437478091", presentation="PresentationDuLieu"
        )
        self.reason = ReasonFactory(description="DescriptionDuMotif")

        self.contact = ClientProfileFactory(
            first_name="Alexandre",
            last_name="Norman",
            phone="0683274463",
            email="norman@xael.org",
        )

        self.contact_rgpd = RgpdConsentFactory(
            user=self.contact,
            allow_to_keep_data=True,
            allow_to_use_email_to_send_reminder=True,
            allow_to_use_phone_number_to_send_reminder=True,
            allow_to_share_my_information_with_my_advisor=True,
            allow_to_share_my_information_with_partners=True,
        )
        for a in [self.advisor1, self.advisor2, self.advisor3]:
            RgpdConsentFactory(
                user=a,
                allow_to_keep_data=True,
                allow_to_use_email_to_send_reminder=True,
                allow_to_use_phone_number_to_send_reminder=True,
                allow_to_share_my_information_with_my_advisor=True,
                allow_to_share_my_information_with_partners=True,
            )

        self.appointment = AppointmentFactory(
            start_date=make_aware(
                datetime.datetime(2019, 9, 15, 12, 10, 0), is_dst=False
            ),
            end_date=make_aware(
                datetime.datetime(2019, 9, 15, 12, 40, 0), is_dst=False
            ),
            advisor=self.advisor1,
            place=self.place,
            reason=self.reason,
            client_or_contact=self.contact,
        )
        self.nm = NotificationManager()

    def test_no_notification_for_other_trigger(self):
        notification = NotificationFactory(
            trigger="created_advisor",
            to="contact",
            term="immediate",
            group=self.group,
            is_active=True,
            term_day_type="calendar",
            term_days=1,
            term_time=datetime.time(12, 0),
            term_after_before="before",
            all_reasons=True,
            all_places=True,
            sms_is_active=True,
            mail_is_active=True,
            chat_is_active=False,
        )
        notification.advisors.add(self.advisor1)
        self.nm.manage_notifications_for_object(
            origin_of_notification=self.appointment,
            trigger_type="created_contact",
            group=self.group,
        )

        ct = ContentType.objects.get_for_model(self.appointment)

        # NotificationRequested does not exist
        self.assertFalse(
            NotificationRequested.objects.filter(
                notification=notification,
                content_type=ct,
                object_id=self.appointment.pk,
            ).exists()
        )

    def test_multi_protocol_notification_send_all_notifications(self):
        # a notification with sms and mail active
        notification = NotificationFactory(
            trigger="created_advisor",
            to="contact",
            term="immediate",
            group=self.group,
            is_active=True,
            term_day_type="calendar",
            term_days=1,
            term_time=datetime.time(12, 0),
            term_after_before="before",
            all_reasons=True,
            all_places=True,
            sms_is_active=True,
            mail_is_active=True,
            chat_is_active=False,
        )
        notification.advisors.add(self.advisor1)
        self.nm.manage_notifications_for_object(
            origin_of_notification=self.appointment,
            trigger_type="created_advisor",
            group=self.group,
        )

        ct = ContentType.objects.get_for_model(self.appointment)

        # NotificationRequested exist
        self.assertTrue(
            NotificationRequested.objects.filter(
                notification=notification,
                content_type=ct,
                object_id=self.appointment.pk,
            ).exists()
        )

        # NotificationRequested are two of them
        self.assertEqual(
            NotificationRequested.objects.filter(
                notification=notification,
                content_type=ct,
                object_id=self.appointment.pk,
            ).count(),
            2,
        )

        # NotificationRequested have been send by sms and mail
        methods = [
            x.exchange.message_type
            for x in NotificationRequested.objects.filter(
                notification=notification,
                content_type=ct,
                object_id=self.appointment.pk,
            )
        ]
        self.assertIn("sms", methods)
        self.assertIn("mail", methods)

        # All have been send to self.contact
        self.assertEqual(
            len(
                [
                    x.exchange.to_account.pk
                    for x in NotificationRequested.objects.filter(
                        notification=notification,
                        content_type=ct,
                        object_id=self.appointment.pk,
                    )
                    if x.exchange.to_account.pk != self.contact.pk
                ]
            ),
            0,
        )

    def test_notification_is_sent_to_contact(self):
        notification = NotificationFactory(
            trigger="created_advisor",
            to="contact",
            term="immediate",
            group=self.group,
            is_active=True,
            term_day_type="calendar",
            term_days=1,
            term_time=datetime.time(12, 0),
            term_after_before="before",
            all_reasons=True,
            all_places=True,
            sms_is_active=False,
            mail_is_active=True,
            chat_is_active=False,
        )
        notification.advisors.add(self.advisor1)
        self.nm.manage_notifications_for_object(
            origin_of_notification=self.appointment,
            trigger_type="created_advisor",
            group=self.group,
        )

        ct = ContentType.objects.get_for_model(self.appointment)

        self.assertTrue(
            NotificationRequested.objects.filter(
                notification=notification,
                content_type=ct,
                object_id=self.appointment.pk,
            ).exists()
        )

        exchange = (
            NotificationRequested.objects.filter(
                notification=notification,
                content_type=ct,
                object_id=self.appointment.pk,
            )
            .last()
            .exchange
        )

        self.assertEqual(exchange.to_account.pk, self.contact.pk)

    def test_notification_is_sent_to_advisor(self):
        notification = NotificationFactory(
            trigger="created_advisor",
            to="allocated_advisor",
            term="immediate",
            group=self.group,
            is_active=True,
            term_day_type="calendar",
            term_days=1,
            term_time=datetime.time(12, 0),
            term_after_before="before",
            all_reasons=True,
            all_places=True,
            sms_is_active=False,
            mail_is_active=True,
            chat_is_active=False,
        )
        notification.advisors.add(self.advisor1)
        self.nm.manage_notifications_for_object(
            origin_of_notification=self.appointment,
            trigger_type="created_advisor",
            group=self.group,
        )

        ct = ContentType.objects.get_for_model(self.appointment)

        self.assertTrue(
            NotificationRequested.objects.filter(
                notification=notification,
                content_type=ct,
                object_id=self.appointment.pk,
            ).exists()
        )

        exchange = (
            NotificationRequested.objects.filter(
                notification=notification,
                content_type=ct,
                object_id=self.appointment.pk,
            )
            .last()
            .exchange
        )

        self.assertEqual(exchange.to_account, self.advisor1)

    def test_inactive_notification_do_not_launch(self):
        notification_for_advisor = NotificationFactory(
            trigger="created_advisor",
            to="all_advisors",
            term="immediate",
            group=self.group,
            is_active=False,
            term_day_type="calendar",
            term_days=1,
            term_time=datetime.time(12, 0),
            term_after_before="before",
            all_reasons=True,
            all_places=True,
            sms_is_active=True,
            mail_is_active=True,
            chat_is_active=True,
        )

        self.nm.manage_notifications_for_object(
            origin_of_notification=self.appointment,
            trigger_type="created_advisor",
            group=self.group,
        )

        ct = ContentType.objects.get_for_model(self.appointment)

        self.assertFalse(
            NotificationRequested.objects.filter(
                notification=notification_for_advisor,
                content_type=ct,
                object_id=self.appointment.pk,
            ).exists()
        )

    def test_wrong_to_raise_exception(self):
        NotificationFactory(
            trigger="created_advisor",
            to="INEXISTING_RECIPIENT",
            term="immediate",
            group=self.group,
            is_active=True,
            term_day_type="calendar",
            term_days=1,
            term_time=datetime.time(12, 0),
            term_after_before="before",
            all_reasons=True,
            all_places=True,
            sms_is_active=True,
            mail_is_active=True,
            chat_is_active=True,
        )
        self.assertRaises(
            ValueError,
            self.nm.manage_notifications_for_object,
            origin_of_notification=self.appointment,
            trigger_type="created_advisor",
            group=self.group,
        )

    def test_multiple_notifications_for_same_event(self):
        notification_for_advisor = NotificationFactory(
            trigger="created_advisor",
            to="all_advisors",
            term="immediate",
            group=self.group,
            is_active=True,
            term_day_type="calendar",
            term_days=1,
            term_time=datetime.time(12, 0),
            term_after_before="before",
            all_reasons=True,
            all_places=True,
            sms_is_active=True,
            mail_is_active=True,
            chat_is_active=True,
        )

        notification_for_contact = NotificationFactory(
            trigger="created_advisor",
            to="contact",
            term="immediate",
            group=self.group,
            is_active=True,
            term_day_type="calendar",
            term_days=1,
            term_time=datetime.time(12, 0),
            term_after_before="before",
            all_reasons=True,
            all_places=True,
            sms_is_active=True,
            mail_is_active=True,
            chat_is_active=True,
        )

        self.nm.manage_notifications_for_object(
            origin_of_notification=self.appointment,
            trigger_type="created_advisor",
            group=self.group,
        )

        ct = ContentType.objects.get_for_model(self.appointment)

        self.assertTrue(
            NotificationRequested.objects.filter(
                notification=notification_for_advisor,
                content_type=ct,
                object_id=self.appointment.pk,
            ).exists()
        )
        self.assertTrue(
            NotificationRequested.objects.filter(
                notification=notification_for_contact,
                content_type=ct,
                object_id=self.appointment.pk,
            ).exists()
        )

    def test_date_to_schedule_notification_for_appointment_immediate(self):
        notification = NotificationFactory(
            trigger="create_advisor",
            to="all_advisors",
            term="immediate",
            group=self.group,
            is_active=True,
            term_day_type="calendar",
            term_days=1,
            term_time=datetime.time(12, 0),
            term_after_before="before",
            all_reasons=True,
            all_places=True,
            sms_is_active=True,
            mail_is_active=True,
            chat_is_active=True,
        )

        with mock.patch("dialogwatt.helpers.notification_manager.date") as mock_date:
            mock_date.today.return_value = datetime.date(2019, 9, 13)
            mock_date.side_effect = lambda *args, **kwargs: datetime.date(
                *args, **kwargs
            )

            self.nm._get_now = mock.MagicMock(
                return_value=make_aware(
                    datetime.datetime(2019, 9, 19, 22, 11, 33), is_dst=False
                )
            )
            # On time
            self.nm._get_now_time = mock.MagicMock(return_value=datetime.time(12, 00))
            self.assertEqual(
                self.nm._date_to_schedule_notification_for_appointment(
                    notification, self.appointment
                ),
                make_aware(datetime.datetime(2019, 9, 19, 22, 11, 33), is_dst=False),
            )

    def test_date_to_schedule_notification_for_appointment_before_time(self):
        notification = NotificationFactory(
            trigger="create_advisor",
            to="all_advisors",
            term="delayed",
            group=self.group,
            is_active=True,
            term_day_type="calendar",
            term_days=1,
            term_time=datetime.time(12, 0),
            term_after_before="before",
            all_reasons=True,
            all_places=True,
            sms_is_active=True,
            mail_is_active=True,
            chat_is_active=True,
        )

        # Before 2 days
        with mock.patch("dialogwatt.helpers.notification_manager.date") as mock_date:
            mock_date.today.return_value = datetime.date(2019, 9, 13)
            mock_date.side_effect = lambda *args, **kwargs: datetime.date(
                *args, **kwargs
            )

            # On time
            self.nm._get_now_time = mock.MagicMock(return_value=datetime.time(12, 00))
            self.assertEqual(
                self.nm._date_to_schedule_notification_for_appointment(
                    notification, self.appointment
                ),
                make_aware(datetime.datetime(2019, 9, 14, 12, 0, 0), is_dst=False),
            )

    def test_date_to_schedule_notification_for_appointment_on_time(self):
        notification = NotificationFactory(
            trigger="create_advisor",
            to="all_advisors",
            term="delayed",
            group=self.group,
            is_active=True,
            term_day_type="calendar",
            term_days=1,
            term_time=datetime.time(12, 0),
            term_after_before="before",
            all_reasons=True,
            all_places=True,
            sms_is_active=True,
            mail_is_active=True,
            chat_is_active=True,
        )

        # On time
        with mock.patch("dialogwatt.helpers.notification_manager.date") as mock_date:
            mock_date.today.return_value = datetime.date(2019, 9, 15)
            mock_date.side_effect = lambda *args, **kwargs: datetime.date(
                *args, **kwargs
            )
            self.nm._get_now = mock.MagicMock(
                return_value=make_aware(
                    datetime.datetime(2019, 9, 19, 22, 11, 33), is_dst=False
                )
            )

            # Before time
            self.nm._get_now_time = mock.MagicMock(return_value=datetime.time(11, 00))
            self.assertEqual(
                self.nm._date_to_schedule_notification_for_appointment(
                    notification, self.appointment
                ),
                make_aware(datetime.datetime(2019, 9, 14, 12, 00, 00), is_dst=False),
            )

            # On time
            self.nm._get_now_time = mock.MagicMock(return_value=datetime.time(12, 00))
            self.assertEqual(
                self.nm._date_to_schedule_notification_for_appointment(
                    notification, self.appointment
                ),
                make_aware(datetime.datetime(2019, 9, 19, 22, 11, 33), is_dst=False),
            )

            # After time
            self.nm._get_now_time = mock.MagicMock(return_value=datetime.time(13, 00))
            self.assertEqual(
                self.nm._date_to_schedule_notification_for_appointment(
                    notification, self.appointment
                ),
                make_aware(datetime.datetime(2019, 9, 19, 22, 11, 33), is_dst=False),
            )

    def test_date_to_schedule_notification_for_appointment_after_time(self):
        notification = NotificationFactory(
            trigger="create_advisor",
            to="all_advisors",
            term="delayed",
            group=self.group,
            is_active=True,
            term_day_type="calendar",
            term_days=1,
            term_time=datetime.time(12, 0),
            term_after_before="before",
            all_reasons=True,
            all_places=True,
            sms_is_active=True,
            mail_is_active=True,
            chat_is_active=True,
        )

        # After time
        with mock.patch("dialogwatt.helpers.notification_manager.date") as mock_date:
            mock_date.today.return_value = datetime.date(2019, 9, 16)
            mock_date.side_effect = lambda *args, **kwargs: datetime.date(
                *args, **kwargs
            )
            self.nm._get_now = mock.MagicMock(
                return_value=make_aware(
                    datetime.datetime(2019, 9, 19, 22, 11, 33), is_dst=False
                )
            )

            # After time
            self.nm._get_now_time = mock.MagicMock(return_value=datetime.time(11, 00))
            self.assertEqual(
                self.nm._date_to_schedule_notification_for_appointment(
                    notification, self.appointment
                ),
                make_aware(datetime.datetime(2019, 9, 14, 12, 00, 00), is_dst=False),
            )

    def test_format_place_name_only(self):
        nm = NotificationManager()

        place = PlaceFactory(
            name="Accueil",
            phone=None,
            address=None,
        )

        self.assertEqual(
            nm._format_place(place),
            "Accueil",
        )

    def test_format_place_no_address(self):
        nm = NotificationManager()

        place = PlaceFactory(
            name="Accueil",
            phone="0437478091",
            address=None,
        )

        self.assertEqual(
            nm._format_place(place),
            "Accueil (téléphone: +33437478091)",
        )

    def test_format_place_no_phone(self):
        nm = NotificationManager()

        place = PlaceFactory(name="Accueil", phone=None, address="14 place JF, Lyon")

        self.assertEqual(
            nm._format_place(place),
            "Accueil (adresse: 14 place JF, Lyon)",
        )

    def test_format_place(self):
        nm = NotificationManager()

        place = PlaceFactory(
            name="Accueil",
            phone="0437478091",
            presentation="PresentationDuLieu",
            address="14 place JF, Lyon",
        )

        self.assertEqual(
            nm._format_place(place),
            "Accueil (adresse: 14 place JF, Lyon / téléphone: +33437478091)",
        )

    def test_replace_tags_in_sms(self):
        notification = NotificationFactory(
            sms_is_active=True,
            sms_message="{contact} {date_rdv} {conseiller} {structure} {tel_structure} {lieu} {tel_lieu} {texte_lieu} {texte_motif} {texte_creneau}",  # NOQA E501
        )
        messages = self.nm._replace_tags_in_text(
            notification, self.contact, self.appointment
        )
        self.assertEqual(
            messages["sms"],
            f"Alexandre Norman 15 septembre 2019, 12:10 - 12:40 Conseiller Test Hespul +33327478090 {self.nm._format_place(self.appointment.place)} +33437478091 PresentationDuLieu DescriptionDuMotif",  # NOQA E501
        )

    def test_replace_tags_in_mail(self):
        notification = NotificationFactory(
            mail_is_active=True,
            mail_message="<b>{contact}</b> {date_rdv} <b>{conseiller}</b> {structure} <ul><li>{tel_structure}</li> <li>{lieu}</li></ul> {tel_lieu} {texte_lieu} {texte_motif} {texte_creneau}",  # NOQA E501
        )
        messages = self.nm._replace_tags_in_text(
            notification, self.contact, self.appointment
        )
        self.assertEqual(
            messages["mail"],
            f"<b>Alexandre Norman</b> 15 septembre 2019, 12:10 - 12:40 <b>Conseiller Test</b> Hespul <ul><li>+33327478090</li> <li>{self.nm._format_place(self.appointment.place)}</li></ul> +33437478091 PresentationDuLieu DescriptionDuMotif",  # NOQA E501
        )

        msg = f"**Alexandre Norman** 15 septembre 2019, 12:10 - 12:40 **Conseiller Test**\nHespul\n\n  * +33327478090\n  * {self.nm._format_place(self.appointment.place)}\n\n+33437478091 PresentationDuLieu DescriptionDuMotif\n\n"  # NOQA E501

        self.assertEqual(messages["mail_ascii"], msg)

    def test_replace_tags_in_chat(self):
        notification = NotificationFactory(
            chat_is_active=True,
            chat_message="{contact} {date_rdv} {conseiller} {structure} {tel_structure} {lieu} {tel_lieu} {texte_lieu} {texte_motif} {texte_creneau}",  # NOQA E501
        )
        messages = self.nm._replace_tags_in_text(
            notification, self.contact, self.appointment
        )
        self.assertEqual(
            messages["chat"],
            f"Alexandre Norman 15 septembre 2019, 12:10 - 12:40 Conseiller Test Hespul +33327478090 {self.nm._format_place(self.appointment.place)} +33437478091 PresentationDuLieu DescriptionDuMotif",  # NOQA E501
            # "Alexandre Norman 15 septembre 2019, 12:10 - 12:40 Conseiller Test Hespul +33327478090 Accueil +33437478091 PresentationDuLieu DescriptionDuMotif ",  # NOQA E501
        )

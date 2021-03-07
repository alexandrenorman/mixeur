# -*- coding: utf-8 -*-

import logging
from datetime import date, datetime

from dateutil.relativedelta import relativedelta

from django.contrib.contenttypes.models import ContentType
from django.db import transaction

import html2text

import pytz

from core.helpers import format_datetime_interval

from dialogwatt.models import Exchange, Notification, NotificationRequested


logger = logging.getLogger(__name__)  # NOQA


class NotificationManager:
    """
    Take care of sending Notification using the best media when needed
    """

    def __init__(self, immediate_only: bool = True):
        """
        Constructor

        :immediate_only: manage notifications that must be sent now if True delayed if False
        """
        self.immediate_only = immediate_only

    def _get_notifications(self, trigger_type=None, group=None):
        notifications = Notification.active.all()
        if trigger_type:
            notifications = notifications.filter(trigger=trigger_type)

        if group:
            notifications = notifications.filter(group=group)

        return notifications

    def manage_notifications_for_object(
        self, origin_of_notification, trigger_type=None, group=None
    ):
        """
        Loop on active notifications for an object and call related functions

        :origin_of_notification: object to activate notification for [User or Appointment]
        :trigger_type: Notification.TRIGGER
        :group: notifications for Group
        """

        ct = ContentType.objects.get_for_model(origin_of_notification)
        ct_model_class = ct.model_class()
        ct_model_class_as_key = ".".join(
            [ct_model_class.__module__, ct_model_class.__name__]
        )

        callbacks = {
            "accounts.models.user.User": {
                "created_account": self._notification_for_user
            },
            "dialogwatt.models.appointment.Appointment": {
                "created_client": self._notification_for_appointment,
                "changed_client": self._notification_for_appointment,
                "cancelled_client": self._notification_for_appointment,
                "created_advisor": self._notification_for_appointment,
                "changed_advisor": self._notification_for_appointment,
                "cancelled_advisor": self._notification_for_appointment,
                "date_of_appointment": self._delayed_notification_for_appointment,
            },
        }

        for notification in self._get_notifications(
            trigger_type=trigger_type, group=group
        ):
            # Continue if Notification has already been send for something
            # else than a change
            if (
                trigger_type is not None
                and "changed" not in trigger_type
                and NotificationRequested.objects.filter(
                    notification=notification,
                    content_type=ct,
                    object_id=origin_of_notification.id,
                ).exists()
            ):
                continue

            try:
                callbacks[ct_model_class_as_key][notification.trigger](
                    notification, origin_of_notification
                )
            except KeyError:
                raise ValueError(
                    f"Undefined notification callback for trigger type [{notification.trigger}] and object {ct_model_class_as_key}"  # NOQA: 501
                )

    def _delayed_notification_for_appointment(self, notification, appointment):
        date_for_notification = self._date_to_schedule_notification_for_appointment(
            notification, appointment
        )
        logger.debug(
            f"NotificationManager : {notification} / {appointment} -> {appointment.start_date} {date_for_notification}"
        )

        if (
            date_for_notification is not None
            and date_for_notification < self._get_now()
        ):
            logger.debug(
                f"NotificationManager : {notification} / {appointment} -> DO notification NOW"
            )
            return self._notification_for_appointment(notification, appointment)

    def _notification_for_appointment(self, notification, appointment):  # NOQA: C901
        date_for_notification = self._date_to_schedule_notification_for_appointment(
            notification, appointment
        )

        # If no notification date, do nothing !
        if date_for_notification is None:
            return

        recipients = None

        if notification.to == "contact":
            recipients = [appointment.client_or_contact]

        elif notification.to == "all_advisors":
            recipients = list(appointment.group.users)

        elif notification.to == "some_advisors":
            recipients = list(notification.advisors.all())

        elif notification.to == "allocated_advisor":
            if appointment.advisor is None:
                return

            recipients = [appointment.advisor]

        if recipients is None:
            raise ValueError(
                f"Configuration error : No recipient for notification {notification.pk}"
            )

        try:
            contact_methods = appointment.client_or_contact.allowed_methods_for_contact
        except AttributeError:
            contact_methods = []

        for to_account in recipients:
            messages = self._replace_tags_in_text(
                notification, appointment.client_or_contact, appointment
            )
            with transaction.atomic():
                callbacks = {
                    "sms": {"prop": "sms_is_active", "call": "send_by_sms"},
                    "mail": {"prop": "mail_is_active", "call": "send_by_email"},
                    "chat": {"prop": "chat_is_active", "call": "send_by_chat"},
                }

                for method in callbacks:
                    if (
                        getattr(notification, callbacks[method]["prop"])
                        and method in contact_methods
                    ):

                        exchange = Exchange.objects.create(
                            from_account=appointment.advisor,
                            to_account=to_account,
                            trigger=notification.trigger,
                            message_type=method,
                            subject=messages["mail_subject"],
                            message_sms=messages["sms"],
                            message_mail_ascii=messages["mail_ascii"],
                            message_mail_html=messages["mail"],
                            schedule=date_for_notification,
                            group=appointment.group,
                        )
                        exchange.save()

                        sending_func = getattr(exchange, callbacks[method]["call"])
                        sending_func()

                        nr = NotificationRequested.objects.create(
                            notification=notification,
                            origin_of_notification=appointment,
                            exchange=exchange,
                        )
                        nr.save()

    def _notification_for_user(self, notification, origin_of_notification):
        # TBD, sur création d'un utilisateur client dans un WhiteLabelling
        # envoyer un mail au groupe concerné
        return

    def _get_now_time(self):
        # Used for allowing mock in tests
        return datetime.now().astimezone(pytz.timezone("Europe/Paris")).time()

    def _get_now(self):
        # Used for allowing mock in tests
        return datetime.now().astimezone(pytz.timezone("Europe/Paris"))

    def _date_to_schedule_notification_for_appointment(self, notification, appointment):
        """"""

        if (
            not notification.all_reasons
            and appointment.reason not in notification.reasons.all()
        ):
            return None

        if (
            not notification.all_places
            and appointment.place not in notification.places.all()
        ):
            return None

        if notification.term == "immediate":
            return self._get_now()

        # delayed
        today = date.today()
        appointment_date = appointment.start_date
        delta = relativedelta(
            days=notification.term_days
            * (-1 if notification.term_after_before == "before" else 1)
        )
        notification_date = appointment_date + delta
        if today >= notification_date.date():

            if self._get_now_time() >= notification.term_time:
                return self._get_now()

        notification_date = notification_date.replace(
            hour=notification.term_time.hour,
            minute=notification.term_time.minute,
            second=0,
            microsecond=0,
        )
        return notification_date

    def _replace_tags_in_text(self, notification, contact, appointment):
        """
        Replace tokens by formatted data from appointment or contact

        returns messages dicts with keys sms, mail, chat and mail_subject containing
        the text with replaced variable
        """
        messages = {
            "sms": notification.sms_message,
            "mail": notification.mail_message,
            "chat": notification.chat_message,
            "mail_subject": notification.mail_subject,
        }

        if appointment.slot is not None:
            public_description = appointment.slot.public_description
        else:
            public_description = None

        if appointment.advisor is not None:
            advisor = appointment.advisor.full_name
        else:
            advisor = ""

        tokens = {
            "{contact}": contact.full_name if contact else "",  # NOQA: FS003
            "{date_rdv}": format_datetime_interval(  # NOQA: FS003
                appointment.start_date, appointment.end_date
            ),
            "{conseiller}": advisor,  # NOQA: FS003
            "{structure}": appointment.group.name or "",  # NOQA: FS003
            "{lieu}": f"{self._format_place(appointment.place)}"  # NOQA: FS003
            if appointment.place
            else "",
            "{tel_structure}": f"{appointment.group.phone}"  # NOQA: FS003
            if appointment.group
            else "",
            "{tel_lieu}": f"{appointment.place.phone}"  # NOQA: FS003
            if appointment.place
            else "",  # NOQA: FS003
            "{texte_lieu}": appointment.place.presentation or ""  # NOQA: FS003
            if appointment.place
            else "",
            "{texte_motif}": appointment.reason.description or ""  # NOQA: FS003
            if appointment.reason
            else "",
            "{texte_creneau}": public_description or "",  # NOQA: FS003
            "{jitsi}": f"<a href=\"https://meet.jit.si/{contact.email.replace('@', '-')}\">https://meet.jit.si/{contact.email.replace('@', '-')}</a>"  # NOQA: FS003,E501
            if contact
            else "",  # NOQA: FS003, E501
        }

        for media in messages:
            for token in tokens:
                try:
                    messages[media] = (
                        messages[media].replace(token, tokens[token]).strip()
                    )
                except AttributeError:
                    pass

        # we may want to strip for sms : messages["sms"] = messages["sms"][:160]
        if messages["mail"] is not None:
            messages["mail_ascii"] = self._strip_html_tags(messages["mail"])
        else:
            messages["mail_ascii"] = ""

        return messages

    def _format_place(self, place):
        if place is None:
            return ""

        text = f"{place.name}"
        if place.address or place.phone:
            text += " ("
            if place.address:
                address = place.address.replace("\n", " - ")
                text += f"adresse: {address}"
            if place.address and place.phone:
                text += " / "
            if place.phone:
                text += f"téléphone: {place.phone}"
            text += ")"
        return text

    def _strip_html_tags(self, html):
        return html2text.html2text(html)

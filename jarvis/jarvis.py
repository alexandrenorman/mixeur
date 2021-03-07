# -*- coding: utf-8 -*-
import datetime
import email
import imaplib
import itertools
import logging
import os
import re

from django.db import transaction

from accounts.models import User

from config.settings import (
    JARVIS_DELETE,
    JARVIS_EMAIL,
    JARVIS_HOST,
    JARVIS_PASSWORD,
    JARVIS_PORT,
)

from fac.models import Contact, Note

from .models import AllowedSender


logger = logging.getLogger(__name__)  # NOQA


def replace_gt_lt(value):
    return value.replace("<", "&lt;").replace(">", "&gt;")


class Jarvis:
    path = "/app/jarvis-logs"

    def __init__(self) -> None:
        if not JARVIS_EMAIL:
            raise ValueError(
                "JARVIS not configured properly (missing env JARVIS_EMAIL)"
            )
        self.logs = []
        self.run_time_filename = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")

    def _logger(self, message):
        logger.warning(message)
        self.logs.append(message)

    @property
    def _username(self) -> str:
        return JARVIS_EMAIL

    @property
    def _password(self) -> str:
        return JARVIS_PASSWORD

    @property
    def _host(self) -> str:
        return JARVIS_HOST

    @property
    def _port(self) -> str:
        return JARVIS_PORT

    def _connect(self):
        mail = imaplib.IMAP4_SSL(self._host, self._port)
        mail.login(self._username, self._password)
        mail.select("Inbox")
        return mail

    def read_mails(self):
        self._logger("Jarvis is reading its mailbox.")
        mail = self._connect()

        response, data = mail.search(None, "ALL")

        for i in data[0].decode("utf-8").split():
            self._logger(f"Jarvis: fetch mail number {i}")
            typ, data = mail.fetch(i, "(RFC822)")
            raw_email = data[0][1]

            self._save_bulk_email(raw_email)

            raw_email_string = raw_email.decode("utf-8")
            email_message = email.message_from_string(raw_email_string)

            mail_from = email_message["from"]
            mail_to = email_message["to"]
            mail_cc = email_message["cc"]

            recipients = f"{mail_from}\n{mail_to}\n{mail_cc}\n"

            self._logger(
                f"Jarvis: recipients : From:{mail_from} / To:{mail_to} / Cc:{mail_cc}"
            )

            emails = self._extract_emails(recipients)

            with transaction.atomic():
                advisors = self._find_advisors(emails)
                for advisor in advisors:
                    contacts = self._find_existing_contacts_for_advisor(advisor, emails)
                    if contacts:
                        self._logger(
                            f"Jarvis: Existing contacts: {', '.join([x.email for x in contacts])} for {advisor.email}"
                        )

                    for contact in contacts:
                        Note.objects.create(
                            owning_group=advisor.group,
                            creator=advisor,
                            linked_object=contact,
                            note=self._format_email(email_message),
                        )

            with transaction.atomic():
                allowed_senders = self._find_allowed_senders(emails)
                for allowed_sender in allowed_senders:
                    contacts = self._find_existing_contacts_for_allowed_sender(
                        allowed_sender, emails
                    )
                    if contacts:
                        self._logger(
                            f"Jarvis: Existing allowed senders: {', '.join([x.email for x in contacts])} for {allowed_sender.email}"  # NOQA: E501
                        )

                    for contact in contacts:
                        Note.objects.create(
                            owning_group=allowed_sender.group,
                            creator=None,
                            linked_object=contact,
                            note=self._format_email(email_message),
                        )

            if JARVIS_DELETE:
                mail.store(i, "+FLAGS", "\\Deleted")

        if JARVIS_DELETE:
            mail.expunge()

        mail.close()
        mail.logout()
        self._save_logs()

    def _save_bulk_email(self, raw_email: str) -> None:
        i = 1
        filename = f"{self.path}/{self.run_time_filename}-{i}.txt"

        while os.path.exists(filename):
            i += 1
            filename = f"{self.path}/{self.run_time_filename}-{i}.txt"

        self._logger(f"Jarvis: Writing file {filename}")
        with open(filename, "wb") as f:
            f.write(raw_email)

    def _save_logs(self) -> None:
        filename = f"{self.path}/{self.run_time_filename}.log"

        i = 0
        while os.path.exists(filename):
            i += 1
            filename = f"{self.path}/{self.run_time_filename}-{i}.log"

        with open(filename, "w") as f:
            f.write("\n".join(self.logs))

    def _format_email(self, email_message: str) -> str:
        subject = email_message["subject"]

        body = ""
        is_html = False

        if email_message.is_multipart():
            for part in email_message.walk():
                ctype = part.get_content_type()
                cdispo = str(part.get("Content-Disposition"))

                # skip any text/html attachments
                if ctype == "text/html" and "attachment" not in cdispo:
                    body = part.get_payload(decode=True)  # decode
                    is_html = True
                    break

            if body == "":
                for part in email_message.walk():
                    ctype = part.get_content_type()
                    cdispo = str(part.get("Content-Disposition"))

                    # skip any text/plain (txt) attachments
                    if ctype == "text/plain" and "attachment" not in cdispo:
                        body = part.get_payload(decode=True)  # decode
                        break
        else:
            # not multipart - i.e. plain text, no attachments, keeping fingers crossed
            body = email_message.get_payload(decode=True)

        mail_from = email_message["from"]
        mail_to = email_message["to"]
        mail_cc = email_message["cc"]

        self._logger(f"{mail_from}")

        date = [x for x in email_message._headers if x[0] == "Date"][0][1]

        body = body.decode("utf-8", "replace")
        if not is_html:
            body = body.replace("\n", "<br>")

        message = f"<p><b>Sujet:</b> {subject}<br><b>Date:</b> {date}<br><b>From:</b> {replace_gt_lt(mail_from)}<br>"

        if mail_to:
            message += f"<b>To:</b> {replace_gt_lt(mail_to)}<br>"

        if mail_cc:
            message += f"<b>CC:</b> {replace_gt_lt(mail_cc)}</p><p>{body}</p>"

        message += f"</p><p>{body}</p>"

        self._logger(message)
        # max note length is 15000
        return message[:15000]

    def _find_allowed_senders(self, emails):
        allowed_senders = AllowedSender.active.filter(email__in=emails).distinct()
        return allowed_senders

    def _find_advisors(self, emails):
        advisors = User.advisors.filter(email__in=emails).distinct()
        return advisors

    def _find_existing_contacts_for_advisor(self, advisor, emails):
        contacts = [
            contact
            for contact in list(
                itertools.chain(*[Contact.objects.filter(email=x) for x in emails])
            )
            if advisor.has_perm("contact.change", contact)
        ]
        return contacts

    def _find_existing_contacts_for_allowed_sender(self, allowed_sender, emails):
        contacts = Contact.objects.filter(
            owning_group=allowed_sender.group, email__in=emails
        )
        return contacts

    def _extract_emails(self, recipients: str):
        email_re = re.compile(
            r"([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)", re.IGNORECASE
        )
        emails = email_re.findall(recipients)
        return emails

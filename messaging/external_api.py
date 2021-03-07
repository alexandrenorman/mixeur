# -*- coding: utf-8 -*-
from django.core.mail import send_mail

from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

import requests
import phonenumbers
import json


def twilio_raw_send(account, token, phone, to_phone, message):
    client = Client(account, token)
    try:
        client.messages.create(body="message", from_=f"{phone}", to=f"{to_phone}")
    except TwilioRestException as e:
        raise SystemError(str(e))


def ovh_raw_send(account, login, password, sender, to_phone, message):
    # to_phone="0033683274463"
    if not str(to_phone).startswith("00"):
        to_phone = f"00{to_phone}"

    url = f"https://www.ovh.com/cgi-bin/sms/http2sms.cgi?&account={account}&login={login}&password={password}&from={sender}&to={to_phone}&message={message}&contentType=application/json"  # NOQA: E50
    r = requests.get(url, timeout=60)
    # r.status_code

    # b"KO\nInvalid smsAccount, it should look like 'sms-ab1234-1'.\n"
    # b'OK\n53.00\n217618864'
    response = json.loads(r.content.decode("utf-8"))

    if response["status"] in [100, 101]:
        # credit = response["creditLeft"]
        sms_ids = response["smsIds"]
        return "OVH-" + ",".join(sms_ids)

    raise SystemError(response["message"] + " " + url)


class TwilioApi:
    def __init__(self, sms_account):
        self.sms_account = sms_account

    def send(self, to_phone, message):
        account = self.sms_account.twilio_account
        token = self.sms_account.twilio_token
        phone = self.sms_account.phone

        twilio_raw_send(account, token, phone, to_phone, message)

        # client = Client(account, token)
        # try:
        #     client.messages.create(
        #         body="message", from_=f"{phone}", to=f"{to_phone}",
        #     )
        # except TwilioRestException as e:
        #     raise SystemError(str(e))


class OvhApi:
    def __init__(self, sms_account):
        self.sms_account = sms_account

    def send(self, to_phone, message):

        account = self.sms_account.ovh_account
        login = self.sms_account.ovh_login
        password = self.sms_account.ovh_password
        sender = self.sms_account.ovh_sender

        to_phone = phonenumbers.parse(to_phone, region="FR").national_number
        to_phone = f"0033{to_phone}"
        ovh_raw_send(account, login, password, sender, to_phone, message)

        # r = requests.get(self._url_for_ovh(to_phone, message))
        # # r.status_code

        # # b"KO\nInvalid smsAccount, it should look like 'sms-ab1234-1'.\n"
        # # b'OK\n53.00\n217618864'
        # response = json.loads(r.content.decode("utf-8"))

        # if response["status"] in [100, 101]:
        #     # credit = response["creditLeft"]
        #     sms_ids = response["smsIds"]
        #     return "OVH-" + ",".join(sms_ids)

        # raise SystemError(response["message"])

    # def _url_for_ovh(self, to_phone, message):
    #     account = self.sms_account.ovh_account
    #     login = self.sms_account.ovh_login
    #     password = self.sms_account.ovh_password
    #     phone = self.sms_account.phone

    #     to_phone = phonenumbers.parse(to_phone, region="FR").national_number
    #     to_phone = f"0033{to_phone}"

    #     url = f"https://www.ovh.com/cgi-bin/sms/http2sms.cgi?&account={account}&login={login}&password={password}&from={phone}&to={to_phone}&message={message}&contentType=application/json"  # NOQA: E501
    #     return url


class MailApi:
    def __init__(self, sms_account):
        self.sms_account = sms_account

    def send(self, to_phone, message):
        send_mail(
            subject=f"sms to {to_phone}",
            from_email="debug@mixeur.local",
            message=message,
            recipient_list=[f"{to_phone}@mixeur.local"],
            html_message=message,
            connection=None,
        )


class SmsApi:
    def __init__(self, sms_account):
        self.sms_account = sms_account
        if self.sms_account.account_type == "twilio":
            self.delegate = TwilioApi(sms_account)

        elif self.sms_account.account_type == "ovh":
            self.delegate = OvhApi(sms_account)

        elif self.sms_account.account_type == "mail":
            self.delegate = MailApi(sms_account)

        else:
            raise ValueError(
                f"Unknown SmsAccount type {sms_account.account_type} [{sms_account.pk}]"
            )

    def send(self, to_phone, message):
        return self.delegate.send(to_phone, message)

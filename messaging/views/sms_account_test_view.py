# -*- coding: utf-8 -*-
import json
from django.core.mail import send_mail
from django.http import JsonResponse
from rest_framework import status

from helpers.views import AdvisorRequiredApiView
from messaging.forms import SmsAccountTestForm

from messaging.external_api import twilio_raw_send, ovh_raw_send


class SmsAccountTestView(AdvisorRequiredApiView):
    """
    SmsAccountTest View
    """

    def post(self, request, *args, **kwargs):
        """
        Create model by [pk]
        """
        object_data = json.loads(request.body)
        form = SmsAccountTestForm(object_data)

        if not form.is_valid():
            return JsonResponse(form.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            account_type = form.cleaned_data["account_type"]
            to_phone = form.cleaned_data["test_phone"]
            message = "Test d'envoi de SMS - DialogWatt"

            if account_type == "twilio":
                account = form.cleaned_data["twilio_account"]
                token = form.cleaned_data["twilio_token"]
                phone = form.cleaned_data["phone"]

                try:
                    twilio_raw_send(account, token, phone, to_phone, message)
                except Exception as e:
                    return JsonResponse(
                        {"__all__": (str(e),)}, status=status.HTTP_400_BAD_REQUEST
                    )

            elif account_type == "ovh":
                account = form.cleaned_data["ovh_account"]
                login = form.cleaned_data["ovh_login"]
                password = form.cleaned_data["ovh_password"]
                sender = form.cleaned_data["ovh_sender"]

                try:
                    ovh_raw_send(account, login, password, sender, to_phone, message)
                except Exception as e:
                    return JsonResponse(
                        {"__all__": (str(e),)}, status=status.HTTP_400_BAD_REQUEST
                    )

            elif account_type == "mail":
                send_mail(
                    subject=f"sms to {to_phone}",
                    message=message,
                    recipient_list=[f"{to_phone}@mixeur.local"],
                    from_email="debug@mixeur.local",
                    html_message=message,
                    connection=None,
                )
                
            return JsonResponse({"OK": "sent"})

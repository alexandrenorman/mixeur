# -*- coding: utf-8 -*-
import json
from django.http import JsonResponse
from rest_framework import status

from helpers.views import AdvisorRequiredApiView

# from sms.models import TwilioAccount
from messaging.forms import TwilioAccountTestForm

from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException


class TwilioAccountTestView(AdvisorRequiredApiView):
    """
    TwilioAccountTest View
    """

    def post(self, request, *args, **kwargs):
        """
        Create model by [pk]
        """
        object_data = json.loads(request.body)
        form = TwilioAccountTestForm(object_data)

        if not form.is_valid():
            return JsonResponse(
                # {"error": f"Error", "__all__": form.errors}, status=status.HTTP_403_FORBIDDEN
                form.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )
        else:
            account = form.cleaned_data["account"]
            token = form.cleaned_data["token"]
            phone = form.cleaned_data["phone"]
            test_phone = form.cleaned_data["test_phone"]

            client = Client(account, token)
            try:
                client.messages.create(
                    body="Test d'envoi de SMS - DialogWatt",
                    from_=f"{phone}",
                    to=f"{test_phone}",
                )
            except TwilioRestException as e:
                return JsonResponse(
                    {"__all__": (str(e),)}, status=status.HTTP_400_BAD_REQUEST
                )

            return JsonResponse({"OK": "sent"})

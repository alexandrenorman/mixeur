# -*- coding: utf-8 -*-
import json
from django.http import JsonResponse
from rest_framework import status

from helpers.views import AdvisorRequiredApiView
from messaging.forms import SmtpAccountTestForm

from django.core.mail import get_connection, send_mail


class SmtpAccountTestView(AdvisorRequiredApiView):
    """
    SmtpAccountTest View
    """

    def post(self, request, *args, **kwargs):
        """
        Create model by [pk]
        """
        object_data = json.loads(request.body)
        form = SmtpAccountTestForm(object_data)

        if not form.is_valid():
            return JsonResponse(form.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            smtp_type = form.cleaned_data["smtp_type"]
            to_email = form.cleaned_data["test_email"]
            message = "Test d'envoi de SMTP - DialogWatt"
            mailgun_apikey = form.cleaned_data["mailgun_apikey"]
            email_host = form.cleaned_data["email_host"]
            email_port = form.cleaned_data["email_port"]
            email_host_user = form.cleaned_data["email_host_user"]
            email_host_password = form.cleaned_data["email_host_password"]
            email_use_tls = form.cleaned_data["email_use_tls"]
            email_use_ssl = form.cleaned_data["email_use_ssl"]

            if smtp_type == "mailgun":
                connection = get_connection(
                    "anymail.backends.mailgun.EmailBackend", api_key=mailgun_apikey
                )
            elif smtp_type == "smtp":
                connection = get_connection(
                    "django.core.mail.backends.smtp.EmailBackend",
                    host=email_host,
                    port=email_port,
                    username=email_host_user,
                    password=email_host_password,
                    use_tls=email_use_tls,
                    use_ssl=email_use_ssl,
                )

            try:
                send_mail(
                    subject=message,
                    message=message,
                    from_email=email_host_user,
                    recipient_list=[to_email],
                    html_message=None,
                    connection=connection,
                )
            except Exception as e:
                return JsonResponse(
                    {"__all__": (str(e),)}, status=status.HTTP_400_BAD_REQUEST
                )

            return JsonResponse({"OK": "sent"})

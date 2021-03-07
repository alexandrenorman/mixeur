# -*- coding: utf-8 -*-
from django.conf.urls import url

from messaging.views import (
    SmtpAccountView,
    SmtpAccountTestView,
    SmsAccountView,
    SmsAccountTestView,
    # TwilioAccountView,
    # TwilioAccountTestView,
)

app_name = "messaging"

urlpatterns = [
    url(r"^smtp-account/$", SmtpAccountView.as_view(), name="smtp_account_list"),
    url(
        r"^smtp-account/(?P<pk>[^/.]+)/$",
        SmtpAccountView.as_view(),
        name="smtp_account_detail",
    ),
    url(
        r"^smtp-account-test/$",
        SmtpAccountTestView.as_view(),
        name="smtp_account_test",
    ),
    url(r"^sms-account/$", SmsAccountView.as_view(), name="sms_account_list"),
    url(
        r"^sms-account/(?P<pk>[^/.]+)/$",
        SmsAccountView.as_view(),
        name="sms_account_detail",
    ),
    url(r"^sms-account-test/$", SmsAccountTestView.as_view(), name="sms_account_test",),
    # url(r"^twilio-account/$", TwilioAccountView.as_view(), name="twilio_account_list"),
    # url(
    #     r"^twilio-account/(?P<pk>[^/.]+)/$",
    #     TwilioAccountView.as_view(),
    #     name="twilio_account_detail",
    # ),
    # url(
    #     r"^twilio-account-test/$",
    #     TwilioAccountTestView.as_view(),
    #     name="twilio_account_test",
    # ),
]

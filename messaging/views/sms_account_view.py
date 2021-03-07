# -*- coding: utf-8 -*-
from django.http import JsonResponse
from rest_framework import status

from helpers.views import ExpertRequiredApiView, ModelView

from messaging.models import SmsAccount
from messaging.forms import SmsAccountForm
from messaging.serializers import SmsAccountSerializer


class SmsAccountView(ModelView, ExpertRequiredApiView):
    """
    SmsAccount View
    """

    model = SmsAccount
    form = SmsAccountForm
    serializer = SmsAccountSerializer
    perm_module = "messaging/smsaccount"
    updated_at_attribute_name = "updated_at"

    def get(self, request, *args, **kwargs):
        """
        """
        try:
            object = self.model.objects.get(group=request.user.group)
        except self.model.DoesNotExist:

            return JsonResponse(None, safe=False)

        perm = self.get_perm_module(request, "GET")
        if perm and not request.user.has_perm(f"{perm}.view", object):
            return JsonResponse(
                {"error": "view not permitted"}, status=status.HTTP_403_FORBIDDEN
            )

        serializer = self.get_serializer(request, "GET")(object)
        return JsonResponse(serializer.data)

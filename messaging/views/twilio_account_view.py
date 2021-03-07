# -*- coding: utf-8 -*-
from django.http import JsonResponse
from rest_framework import status

from helpers.views import AdvisorRequiredApiView, ModelView

from messaging.models import TwilioAccount
from messaging.forms import TwilioAccountForm
from messaging.serializers import TwilioAccountSerializer


class TwilioAccountView(ModelView, AdvisorRequiredApiView):
    """
    TwilioAccount View
    """

    model = TwilioAccount
    form = TwilioAccountForm
    serializer = TwilioAccountSerializer
    perm_module = "messaging/twilioaccount"
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

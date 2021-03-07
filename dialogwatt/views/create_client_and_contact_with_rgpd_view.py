# -*- coding: utf-8 -*-
import json

from django.db import transaction
from django.http import JsonResponse

from rest_framework import status

import serpy

from accounts.forms import RgpdConsentForm, UserForm
from accounts.serializers import RgpdConsentSerializer, UserSerializer

from fac.forms import ContactForm
from fac.serializers import ContactSerializer

from helpers.views import ExpertRequiredApiView

from white_labelling.models import WhiteLabelling


class UserAndContactAndRgpdConsentSerializer(serpy.DictSerializer):
    user = UserSerializer()
    contact = ContactSerializer()
    rgpd_consent = RgpdConsentSerializer()
    domain_name = serpy.Field(required=False)


class CreateClientAndContactWithRgpdView(ExpertRequiredApiView):
    """
    Create a client and a contact in the same view
    """

    def post(self, request, *args, **kwargs):
        json_data = json.loads(request.body)
        user_data = json_data["user"]
        rgpd_consent_data = json_data["rgpd_consent"]
        domain_name_data = json_data["domain_name"]

        with transaction.atomic():
            user_data["user_type"] = "client"
            form = UserForm(user_data)
            if form.is_valid():
                user = form.save()
            else:
                return JsonResponse(form.errors, status=status.HTTP_400_BAD_REQUEST)

            try:
                white_labelling = WhiteLabelling.objects.get(domain=domain_name_data)
            except:  # NOQA
                pass
            else:
                user.white_labelling = white_labelling
                user.save()

            # Always create new instance
            rgpd_consent_data["user"] = user.pk
            form = RgpdConsentForm(rgpd_consent_data)
            if form.is_valid():
                rgpd_consent = form.save()
            else:
                return JsonResponse(form.errors, status=status.HTTP_400_BAD_REQUEST)

            user.is_active = True
            user.save()

            if "nomail" not in json_data:
                user.send_initialize_account_url()

            if user_data["owning_group"]:
                group = user_data["owning_group"]
            else:
                group = request.user.group.pk

            contact_data = {
                "civility": "-",
                "owning_group": group,
                "first_name": user_data["first_name"],
                "last_name": user_data["last_name"],
                "email": user_data["email"],
                "phone": user_data["phone"],
                "lat": 0,
                "lon": 0,
            }

            form = ContactForm(contact_data)

            if form.is_valid():
                contact = form.save()
            else:
                return JsonResponse(form.errors, status=status.HTTP_400_BAD_REQUEST)

        instance = {"user": user, "rgpd_consent": rgpd_consent, "contact": contact}

        serializer = UserAndContactAndRgpdConsentSerializer(instance)
        return JsonResponse(serializer.data)

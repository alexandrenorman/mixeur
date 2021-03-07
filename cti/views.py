# -*- coding: utf-8 -*-

from django.db.models import Q
from django.http import JsonResponse

import phonenumbers

from rest_framework import status

from accounts.models import User

from fac.models import Contact, Organization

from helpers.views import ExpertRequiredApiView

from .serializers import CtiSerializer


class CtiView(ExpertRequiredApiView):
    def get(self, request, phone):

        current_user = request.user
        phone = "".join([x for x in phone if x in "+0123456789"])

        try:
            phone_number = phonenumbers.parse(phone, "FR")
        except ValueError:
            return JsonResponse(
                {"error": "object not found, not a phone number"},
                status=status.HTTP_404_NOT_FOUND,
            )
        except phonenumbers.NumberParseException:
            return JsonResponse(
                {"error": "object not found, not a phone number"},
                status=status.HTTP_404_NOT_FOUND,
            )

        phone = f"0{phone_number.national_number}"

        contacts = [
            contact
            for contact in Contact.objects.filter(
                Q(phone_cache__contains=phone)
                | Q(mobile_phone_cache__contains=phone)
                | Q(fax_cache__contains=phone)
            )
            if current_user.has_perm("fac/contact.view", contact)
        ]
        organizations = [
            organization
            for organization in Organization.objects.filter(
                Q(phone_cache__contains=phone) | Q(fax_cache__contains=phone)
            )
            if current_user.has_perm("fac/organization.view", organization)
        ]

        users = User.objects.filter(
            is_active=True, phone_cache__contains=phone
        ).exclude(
            pk__in=[
                x.client_account.pk for x in contacts if x.client_account is not None
            ]
        )

        serializer = CtiSerializer(
            {
                "q": phone,
                "contacts": contacts,
                "organizations": organizations,
                "users": users,
            }
        )

        return JsonResponse(serializer.data, safe=False)

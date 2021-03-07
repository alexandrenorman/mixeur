# -*- coding: utf-8 -*-
import json

from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from phonenumbers import PhoneNumber

from rest_framework import status

from core.forms import SearchForm

from fac.forms import ContactForm, RgpdConsentForContactsForm
from fac.models import Contact, RgpdConsentForContacts
from fac.serializers import ContactAndRgpdConsentSerializer

from helpers.views import ExpertRequiredApiView, ModelView


class ContactAndRgpdConsentView(ModelView, ExpertRequiredApiView):
    """
    ContactView requires authenticated user

    get :model:`fac.Contact`

    """

    model = Contact
    form = ContactForm
    serializer = ContactAndRgpdConsentSerializer
    perm_module = "fac/contact"

    def list(self, request, *args, **kwargs):  # NOQA: A003
        contacts = Contact.objects.filter(owning_group=request.user.group)

        if "q" in request.GET:
            query_form = SearchForm(request.GET)
            if not query_form.is_valid():
                return JsonResponse(
                    {"__all__": ["Paramêtre de recherche invalide"]},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            query = query_form.cleaned_data["q"]

            # Hack for searching phone numbers
            if "" == "".join([x for x in query if x not in " +0123456789"]):
                query = "".join([x for x in query if x in "+0123456789"])

            for word in query.split():
                try:
                    phone_number = PhoneNumber(word)  # NOQA: F841
                except ValueError:
                    contacts = contacts.filter(
                        Q(last_name__icontains=word)
                        | Q(first_name__icontains=word)
                        | Q(email__icontains=word)
                    )
                else:
                    contacts = contacts.filter(
                        Q(phone_cache__icontains=word)
                        | Q(mobile_phone_cache__icontains=word)
                        | Q(fax_cache__icontains=word)
                    )

        contacts = contacts.distinct()

        perm = self.get_perm_module(request, "LIST")
        if perm:
            allowed_contacts = [
                x for x in contacts if request.user.has_perm(f"{perm}.view", x)
            ]
        else:
            allowed_contacts = contacts

        serializer = self.get_serializer(request, "LIST")(allowed_contacts, many=True)

        return JsonResponse(serializer.data, safe=False)

    def __get_contact_according_to_perm(self, request, pk):
        """
        Get contact or raise PermissionDenied if wrong auth
        """
        if request.user.is_anonymous:
            raise PermissionDenied

        contact = Contact.objects.get(pk=pk, is_active=True)

        if not request.user.has_perm("contact.change", contact):
            raise PermissionDenied("Contact")

        return contact

    def __get_rgpdconsent_according_to_perm(self, request, pk):
        """
        Get rgpdconsent or raise PermissionDenied if wrong auth
        """
        if request.user.is_anonymous:
            raise PermissionDenied("RgpdConsent")

        rgpdconsents = RgpdConsentForContacts.objects.filter(
            contact__is_active=True, contact__pk=pk
        )

        if rgpdconsents.exists():
            rgpdconsent = rgpdconsents.first()
        else:
            rgpdconsent = RgpdConsentForContacts.objects.create(
                contact=Contact.objects.get(pk=pk)
            )

        if not request.user.has_perm("rgpdconsent.change", rgpdconsent):
            raise PermissionDenied("RgpdConsentForContacts")

        return rgpdconsent

    def get(self, request, *args, **kwargs):
        try:
            pk = kwargs["pk"]
        except KeyError:
            pk = request.user.pk
        else:
            contact = get_object_or_404(Contact, pk=pk)

        contact = self.__get_contact_according_to_perm(request, pk)
        rgpd_consent = self.__get_rgpdconsent_according_to_perm(request, pk)

        instance = {"contact": contact, "rgpd_consent": rgpd_consent}

        serializer = ContactAndRgpdConsentSerializer(instance)
        return JsonResponse(serializer.data)

    def post(self, request, *args, **kwargs):
        json_data = json.loads(request.body)
        contact_data = json_data["contact"]
        rgpd_consent_data = json_data["rgpd_consent"]
        owning_group = request.user.group

        with transaction.atomic():
            contact_data["owning_group"] = owning_group.pk
            form = ContactForm(contact_data)
            if form.is_valid():
                contact = form.save()
            else:
                return JsonResponse(form.errors, status=status.HTTP_400_BAD_REQUEST)

            # Always create new instance
            rgpd_consent_data["contact"] = contact.pk
            form = RgpdConsentForContactsForm(rgpd_consent_data)
            if form.is_valid():
                rgpd_consent = form.save()
            else:
                return JsonResponse(form.errors, status=status.HTTP_400_BAD_REQUEST)

            contact.save()

        instance = {"contact": contact, "rgpd_consent": rgpd_consent}

        serializer = ContactAndRgpdConsentSerializer(instance)
        return JsonResponse(serializer.data)

    def patch(self, request, *args, **kwargs):
        try:
            key = kwargs["pk"]
        except KeyError:
            return JsonResponse(
                {"Error": "Not Found"}, status=status.HTTP_404_NOT_FOUND
            )

        # TODO : check permissions
        json_data = json.loads(request.body)
        contact_data = json_data["contact"]
        rgpd_consent_data = json_data["rgpd_consent"]

        pk = key
        contact = get_object_or_404(Contact, pk=pk)

        rgpd_consent_data["contact"] = contact.pk

        # Contact owning_group cannot be changed !
        if contact.owning_group:
            contact_data["owning_group"] = contact.owning_group.pk
        else:
            contact_data["owning_group"] = None

        if "is_active" not in contact_data:
            contact_data["is_active"] = contact.is_active

        with transaction.atomic():
            form = ContactForm(contact_data, instance=contact)
            if form.is_valid():
                form.save()
            else:
                return JsonResponse(form.errors, status=status.HTTP_400_BAD_REQUEST)

            # Always create new instance
            form = RgpdConsentForContactsForm(rgpd_consent_data)
            if form.is_valid():
                form.save()
            else:
                return JsonResponse(form.errors, status=status.HTTP_400_BAD_REQUEST)

        return self.get(request)

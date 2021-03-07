# -*- coding: utf-8 -*-
import serpy

from fac.models import Contact
from fac.serializers.tag_select_serializer import TagSelectSerializer

from helpers.serializers import (
    AutoModelSerializer,
    FaxSerializerMixin,
    MobilePhoneSerializerMixin,
    PhoneSerializerMixin,
)

from .user_select_serializer import UserSelectSerializer


class ContactSerializer(
    AutoModelSerializer,
    PhoneSerializerMixin,
    MobilePhoneSerializerMixin,
    FaxSerializerMixin,
):
    model = Contact
    exclude = [
        "contactsduplicate",
        "contactsduplicate_set",
        "filecontact",
        "filecontact_set",
        "list",
        "list_set",
        "memberoforganization",
        "memberoforganization_set",
        "notecontact",
        "notecontact_set",
        "fileimport_contacts_not_updated",
        "rgpdconsentforcontacts",
        "files",
        "notes",
        "ecorenover_simulations",
    ]
    is_contact = serpy.MethodField()
    is_client = serpy.MethodField()
    roles = serpy.MethodField()

    def get_custom_form_data(self, obj):
        if obj.custom_form_data is None:
            return {}

        return obj.custom_form_data

    def get_owning_group(self, obj):
        return obj.owning_group.pk

    def get_client_account(self, obj):
        if obj.client_account:
            return obj.client_account.pk

    def get_full_name(self, obj):
        return obj.full_name

    def get_is_contact(self, obj):
        return obj.is_contact

    def get_is_client(self, obj):
        return obj.is_client

    def get_tags(self, obj):
        return TagSelectSerializer(obj.tags.all(), many=True).data

    def get_duration_by_project(self, obj):
        return obj.get_duration_by_project()

    def get_referents(self, obj):
        return UserSelectSerializer(obj.referents.all(), many=True).data

    def get_roles(self, obj):
        return [
            {
                "title": member.title_in_organization,
                "organization": member.organization.name,
            }
            for member in obj.memberoforganization_set.all()
        ]

    def get_prefered_address(self, obj):
        if not obj.address:
            try:
                address = [
                    x.organization.address
                    for x in obj.memberoforganization_set.all()
                    if x.use_address_from_organization
                ][0]
            except IndexError:
                return obj.address

            return address

        return obj.address

    def get_lat(self, obj):
        if obj.lat == 0:
            try:
                lat, lon = [
                    (x.organization.lat, x.organization.lon)
                    for x in obj.memberoforganization_set.all()
                    if x.use_address_from_organization
                ][0]
            except IndexError:
                return obj.lat

            return lat

        return obj.lat

    def get_lon(self, obj):
        if obj.lon == 0:
            try:
                lat, lon = [
                    (x.organization.lat, x.organization.lon)
                    for x in obj.memberoforganization_set.all()
                    if x.use_address_from_organization
                ][0]
            except IndexError:
                return obj.lon

            return lon

        return obj.lon

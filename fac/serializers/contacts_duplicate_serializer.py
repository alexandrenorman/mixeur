# -*- coding: utf-8 -*-
from helpers.serializers import AutoModelSerializer
from fac.models import ContactsDuplicate


class ContactsDuplicateSerializer(AutoModelSerializer):
    model = ContactsDuplicate

    def get_owning_group(self, obj):
        return obj.owning_group.pk

    def get_contacts(self, obj):
        contacts = obj.contacts.all()
        return self._get_pk(contacts)

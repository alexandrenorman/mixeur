# -*- coding: utf-8 -*-
from helpers.serializers import AutoModelSerializer
from fac.models import FileImport


class FileImportSerializer(AutoModelSerializer):
    model = FileImport

    def get_owning_group(self, obj):
        return obj.owning_group.pk

    def get_organizations_not_updated(self, obj):
        organizations_not_updated = obj.organizations_not_updated.all()
        return self._get_pk(organizations_not_updated)

    def get_contacts_not_updated(self, obj):
        contacts_not_updated = obj.contacts_not_updated.all()
        return self._get_pk(contacts_not_updated)

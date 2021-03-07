# -*- coding: utf-8 -*-
from fac.models import List
from helpers.serializers import AutoModelSerializer


class ListSerializer(AutoModelSerializer):
    model = List

    def get_owning_group(self, obj):
        return obj.owning_group.pk

    def get_nb_contacts(self, obj):
        return obj.nb_contacts

    def get_contacts(self, obj):
        contacts = obj.contacts.all()
        return [{"pk": contact.pk, "name": contact.full_name} for contact in contacts]

    def get_organizations(self, obj):
        organizations = obj.organizations.all()
        return [
            {"pk": organization.pk, "name": organization.name}
            for organization in organizations
        ]

    def get_lists(self, obj):
        lists = obj.lists.all()
        return [{"pk": _list.pk, "name": _list.title} for _list in lists]

    def get_tags(self, obj):
        tags = obj.tags.all()
        return [{"pk": tag.pk, "name": tag.name} for tag in tags]

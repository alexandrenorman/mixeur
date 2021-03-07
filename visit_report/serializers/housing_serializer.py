# -*- coding: utf-8 -*-
from helpers.serializers import AutoModelSerializer
from visit_report.models import Housing
from fac.models import Contact, Organization


class HousingSerializer(AutoModelSerializer):
    model = Housing

    exclude = ["content_type", "contact_or_organization_id", "user"]

    def get_report(self, obj):
        if hasattr(obj, "report"):
            return obj.report.pk

    def get_contact_entity(self, obj):
        contact_entity = obj.contact_entity
        if contact_entity:
            if obj.content_type.model == "contact":
                name = contact_entity.full_name
            else:
                name = contact_entity.name
            if type(contact_entity) is Contact:
                return {
                    "type": "contact",
                    "pk": obj.contact_or_organization_id,
                    "name": name,
                }
            if type(contact_entity) is Organization:
                return {
                    "type": "organization",
                    "pk": obj.contact_or_organization_id,
                    "name": name,
                }
        return

    def get_groups(self, obj):
        groups = obj.groups.all()
        return self._get_pk(groups)

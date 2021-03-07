import serpy

from fac.models import Contact, Organization
from fac.serializers.tag_select_serializer import TagSelectSerializer


class ContactableSerializer(serpy.Serializer):
    """Serializer for either a `Contact` or an `Organization`"""

    pk = serpy.MethodField()
    type = serpy.MethodField()
    name = serpy.MethodField()
    city = serpy.MethodField()
    phone = serpy.MethodField()
    tags = serpy.MethodField()
    owning_group = serpy.MethodField()

    def get_pk(self, contactable):
        return contactable.pk

    def get_owning_group(self, contactable):
        return contactable.owning_group.pk

    def get_type(self, contactable):
        if isinstance(contactable, Contact):
            return "contact"
        if isinstance(contactable, Organization):
            return "organization"

    def get_name(self, contactable):
        if isinstance(contactable, Contact):
            return f"{contactable.last_name} {contactable.first_name}"
        if isinstance(contactable, Organization):
            return contactable.name

    def get_city(self, contactable):
        return contactable.town

    def get_phone(self, contactable):
        if isinstance(contactable, Contact):
            return contactable.phone_cache or contactable.mobile_phone_cache
        return contactable.phone_cache

    def get_tags(self, contactable):
        return TagSelectSerializer(contactable.tags.all(), many=True).data

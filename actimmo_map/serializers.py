# -*- coding: utf-8 -*-
import serpy
from helpers.serializers import AutoModelSerializer, PhoneSerializerMixin
from actimmo_map.models import ActimmoMap, ActimmoContact

# from accounts.serializers import GroupSimpleWithoutAdminGroupSerializer


class GroupSerializer(serpy.Serializer):
    pk = serpy.Field()
    name = serpy.Field()
    display_name = serpy.MethodField()
    profile_pic = serpy.MethodField()
    website = serpy.Field(required=False)

    def get_profile_pic(self, obj):
        if obj.profile_pic:
            return obj.profile_pic.url
        else:
            return None

    def get_display_name(self, obj):
        return obj.display_name


class ActimmoContactSerializer(PhoneSerializerMixin, AutoModelSerializer):
    model = ActimmoContact
    exclude = [
        "group_presentation",
        "group_profile_pic_overide",
        "group_name_overide",
        "group_website_overide",
    ]
    include_properties = True

    def get_group(self, obj):
        group = obj.group
        serializer = GroupSerializer(group)
        return serializer.data

    def get_group_profile_pic(self, obj):
        if obj.group_profile_pic:
            return obj.group_profile_pic.url
        else:
            return None


class ActimmoMapSerializer(AutoModelSerializer):
    model = ActimmoMap
    exclude = ["groups"]

    def get_contacts(self, obj):
        contacts = []
        for group in obj.groups.all().order_by("full_name"):
            for contact in group.actimmo_contact.all():
                contacts.append(contact)

        serializer = ActimmoContactSerializer(contacts, many=True)
        return serializer.data

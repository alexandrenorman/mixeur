# -*- coding: utf-8 -*-
from accounts.serializers import UserSerializer

from helpers.serializers import AutoModelSerializer

from listepro.models import Professional

from .activity_serializer import ActivitySerializer
from .job_serializer import JobSerializer
from .key_word_serializer import KeyWordSerializer
from .segment_serializer import SegmentSerializer
from .sub_mission_serializer import SubMissionSerializer


class ProfessionalSerializer(AutoModelSerializer):
    model = Professional

    def get_job(self, obj):
        """
        get field job of type ForeignKey
        """
        job = obj.job
        serializer = JobSerializer(job)
        return serializer.data

    def get_segments(self, obj):
        """
        get field segments of type ManyToManyField
        """
        segments = obj.segments.all()
        serializer = SegmentSerializer(segments, many=True)
        return serializer.data

    def get_activity_first(self, obj):
        """
        get field activity_first of type ForeignKey
        """
        activity_first = obj.activity_first
        serializer = ActivitySerializer(activity_first)
        return serializer.data

    def get_activity_second(self, obj):
        """
        get field activity_second of type ForeignKey
        """
        if obj.activity_second is None:
            return None
        activity_second = obj.activity_second
        serializer = ActivitySerializer(activity_second)
        return serializer.data

    def get_activity_third(self, obj):
        """
        get field activity_third of type ForeignKey
        """
        if obj.activity_third is None:
            return None
        activity_third = obj.activity_third
        serializer = ActivitySerializer(activity_third)
        return serializer.data

    def get_activity_fourth(self, obj):
        """
        get field activity_fourth of type ForeignKey
        """
        if obj.activity_fourth is None:
            return None
        activity_fourth = obj.activity_fourth
        serializer = ActivitySerializer(activity_fourth)
        return serializer.data

    def get_primary_key_words(self, obj):
        """
        get field primary_key_words of type ManyToManyField
        """
        primary_key_words = obj.primary_key_words.all()
        serializer = KeyWordSerializer(primary_key_words, many=True)
        return serializer.data

    def get_secondary_key_words(self, obj):
        """
        get field secondary_key_words of type ManyToManyField
        """
        secondary_key_words = obj.secondary_key_words.all()
        serializer = KeyWordSerializer(secondary_key_words, many=True)
        return serializer.data

    def get_sub_missions(self, obj):
        """
        get field sub_missions of type ManyToManyField
        """
        sub_missions = obj.sub_missions.all()
        serializer = SubMissionSerializer(sub_missions, many=True)
        return serializer.data

    def get_user(self, obj):
        """
        get field user of type ForeignKey
        """
        user = obj.user
        serializer = UserSerializer(user)
        return serializer.data

    def get_phone_number(self, obj):
        """
        get field phone_number of type PhoneNumberField
        """
        if obj.phone_number:
            return f"{obj.phone_number}"
        else:
            return ""

    def get_logo(self, obj):
        if obj.logo:
            return obj.logo.url
        else:
            return None

    def get_original_logo(self, obj):
        if obj.original_logo:
            return obj.original_logo.url
        else:
            return None

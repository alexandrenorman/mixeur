# -*- coding: utf-8 -*-
from helpers.serializers import AutoModelSerializer
from experiences.models import Experience

# from experiences.serializers.tag_select_serializer import TagSelectSerializer

from .assignment_tag_serializer import AssignmentTagSerializer
from .experience_sponsor_serializer import ExperienceSponsorSerializer
from .experience_tag_serializer import ExperienceTagSerializer
from .job_tag_serializer import JobTagSerializer
from .partner_tag_serializer import PartnerTagSerializer
from .public_tag_serializer import PublicTagSerializer
from .year_tag_serializer import YearTagSerializer

from accounts.serializers.user_simple_serializer import UserSimpleSerializer

from helpers.strings import truncate_html


class ExperienceSerializer(AutoModelSerializer):
    model = Experience
    referent = UserSimpleSerializer(required=False)

    def get_owning_group(self, obj):
        return obj.owning_group.pk

    def get_assignments(self, obj):
        assignments = obj.assignments.all()
        serializer = AssignmentTagSerializer(assignments, many=True)
        return serializer.data

    def get_sponsors(self, obj):
        sponsors = obj.sponsors.all()
        serializer = ExperienceSponsorSerializer(sponsors, many=True)
        return serializer.data

    def get_jobs(self, obj):
        jobs = obj.jobs.all()
        serializer = JobTagSerializer(jobs, many=True)
        return serializer.data

    def get_partners(self, obj):
        partners = obj.partners.all()
        serializer = PartnerTagSerializer(partners, many=True)
        return serializer.data

    def get_publics(self, obj):
        publics = obj.publics.all()
        serializer = PublicTagSerializer(publics, many=True)
        return serializer.data

    def get_tags(self, obj):
        tags = obj.tags.all()
        serializer = ExperienceTagSerializer(tags, many=True)
        return serializer.data

    def get_years(self, obj):
        years = obj.years.all()
        serializer = YearTagSerializer(years, many=True)
        return serializer.data

    def get_image1(self, obj):
        if obj.image1:
            return obj.image1.url
        else:
            return None

    def get_image2(self, obj):
        if obj.image2:
            return obj.image2.url
        else:
            return None

    def get_description_truncated(self, obj):
        return truncate_html(obj.description, length=200, ellipsis=" […]")

    def get_role_truncated(self, obj):
        return truncate_html(obj.role, length=200, ellipsis=" […]")

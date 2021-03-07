# -*- coding: utf-8 -*-
from django.db.models import Q

from helpers.views import ExpertRequiredApiView, ModelView

from experiences.models import (
    Experience,
    ExperienceSponsor,
    AssignmentTag,
    ExperienceTag,
    JobTag,
    PartnerTag,
    PublicTag,
    YearTag,
)
from experiences.forms import ExperienceForm
from experiences.serializers import ExperienceSerializer, ExperienceCSVSerializer


class ExperienceView(ModelView, ExpertRequiredApiView):
    """
    Experience View
    """

    model = Experience
    form = ExperienceForm
    # serializer = ExperienceSerializer
    perm_module = "experiences/experience"
    updated_at_attribute_name = "updated_at"

    def filter(self, request, queryset):
        """
        Filter queryset from request argument
        """
        pks = request.GET.get("pks")

        assignment = request.GET.get("assignment")
        job = request.GET.get("job")
        partner = request.GET.get("partner")
        public = request.GET.get("public")
        sponsor = request.GET.get("sponsor")
        tag = request.GET.get("tag")
        year = request.GET.get("year")

        query = request.GET.get("q")

        if pks:
            queryset = queryset.filter(pk__in=pks.split(","))

        if assignment:
            queryset = queryset.filter(assignments__pk__in=[assignment])

        if job:
            queryset = queryset.filter(jobs__pk__in=[job])

        if partner:
            queryset = queryset.filter(partners__pk__in=[partner])

        if public:
            queryset = queryset.filter(publics__pk__in=[public])

        if sponsor:
            queryset = queryset.filter(sponsors__sponsor__pk__in=[sponsor])

        if tag:
            queryset = queryset.filter(tags__pk__in=[tag])

        if year:
            queryset = queryset.filter(years__pk__in=[year])

        if query:
            queryset = queryset.filter(
                Q(title__icontains=query)
                | Q(assignments__name__icontains=query)
                | Q(description__icontains=query)
                | Q(description_en__icontains=query)
                | Q(jobs__name__icontains=query)
                | Q(partners__name__icontains=query)
                | Q(publics__name__icontains=query)
                | Q(role__icontains=query)
                | Q(sponsors__sponsor__name__icontains=query)
                | Q(tags__name__icontains=query)
                | Q(years__name__icontains=query)
            ).distinct()

        return queryset

    def get_serializer(self, request, call):
        if request.GET.get("csv") == "1":
            return ExperienceCSVSerializer

        return ExperienceSerializer

    def post_save(self, request, instance, data, created):
        """
        Save object's M2M fields
        """
        for name, obj in [
            ("tags", ExperienceTag),
            ("assignments", AssignmentTag),
            ("sponsors", ExperienceSponsor),
            ("jobs", JobTag),
            ("partners", PartnerTag),
            ("publics", PublicTag),
            ("years", YearTag),
        ]:
            self._save_m2m_from_select(
                instance=instance,
                attribute=name,
                model_queryset=obj.objects,
                data=data.get(name, []),
                track_by="pk",
            )

        # clean deleted ExperienceSponsor
        ExperienceSponsor.objects.filter(experience_sponsors=None).delete()

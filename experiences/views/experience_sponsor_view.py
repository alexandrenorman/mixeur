# -*- coding: utf-8 -*-
from helpers.views import ExpertRequiredApiView, ModelView

from experiences.models import ExperienceSponsor
from experiences.forms import ExperienceSponsorForm
from experiences.serializers import ExperienceSponsorSerializer


class ExperienceSponsorView(ModelView, ExpertRequiredApiView):
    """
    ExperienceSponsor View
    """

    model = ExperienceSponsor
    form = ExperienceSponsorForm
    serializer = ExperienceSponsorSerializer
    perm_module = "experiences/experiencesponsor"
    updated_at_attribute_name = "updated_at"

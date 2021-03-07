# -*- coding: utf-8 -*-
from helpers.views import ExpertRequiredApiView, ModelView

from experiences.models import ExperienceTag
from experiences.forms import ExperienceTagForm
from experiences.serializers import ExperienceTagSerializer


class ExperienceTagView(ModelView, ExpertRequiredApiView):
    """
    ExperienceTag View
    """

    model = ExperienceTag
    form = ExperienceTagForm
    serializer = ExperienceTagSerializer
    perm_module = "experiences/experiencetag"
    updated_at_attribute_name = "updated_at"

# -*- coding: utf-8 -*-
from helpers.views import ExpertRequiredApiView, ModelView

from experiences.models import JobTag
from experiences.forms import JobTagForm
from experiences.serializers import JobTagSerializer


class JobTagView(ModelView, ExpertRequiredApiView):
    """
    JobTag View
    """

    model = JobTag
    form = JobTagForm
    serializer = JobTagSerializer
    perm_module = "experiences/jobtag"
    updated_at_attribute_name = "updated_at"

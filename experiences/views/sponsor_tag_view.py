# -*- coding: utf-8 -*-
from helpers.views import ExpertRequiredApiView, ModelView

from experiences.models import SponsorTag
from experiences.forms import SponsorTagForm
from experiences.serializers import SponsorTagSerializer


class SponsorTagView(ModelView, ExpertRequiredApiView):
    """
    SponsorTag View
    """

    model = SponsorTag
    form = SponsorTagForm
    serializer = SponsorTagSerializer
    perm_module = "experiences/sponsortag"
    updated_at_attribute_name = "updated_at"

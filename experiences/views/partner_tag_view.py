# -*- coding: utf-8 -*-
from helpers.views import ExpertRequiredApiView, ModelView

from experiences.models import PartnerTag
from experiences.forms import PartnerTagForm
from experiences.serializers import PartnerTagSerializer


class PartnerTagView(ModelView, ExpertRequiredApiView):
    """
    PartnerTag View
    """

    model = PartnerTag
    form = PartnerTagForm
    serializer = PartnerTagSerializer
    perm_module = "experiences/partnertag"
    updated_at_attribute_name = "updated_at"

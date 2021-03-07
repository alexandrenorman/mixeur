# -*- coding: utf-8 -*-
from helpers.views import ExpertRequiredApiView, ModelView

from experiences.models import PublicTag
from experiences.forms import PublicTagForm
from experiences.serializers import PublicTagSerializer


class PublicTagView(ModelView, ExpertRequiredApiView):
    """
    PublicTag View
    """

    model = PublicTag
    form = PublicTagForm
    serializer = PublicTagSerializer
    perm_module = "experiences/publictag"
    updated_at_attribute_name = "updated_at"

# -*- coding: utf-8 -*-
from helpers.views import ExpertRequiredApiView, ModelView

from experiences.models import YearTag
from experiences.forms import YearTagForm
from experiences.serializers import YearTagSerializer


class YearTagView(ModelView, ExpertRequiredApiView):
    """
    YearTag View
    """

    model = YearTag
    form = YearTagForm
    serializer = YearTagSerializer
    perm_module = "experiences/yeartag"
    updated_at_attribute_name = "updated_at"

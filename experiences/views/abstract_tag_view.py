# -*- coding: utf-8 -*-
from helpers.views import ExpertRequiredApiView, ModelView

from experiences.models import AbstractTag
from experiences.forms import AbstractTagForm
from experiences.serializers import AbstractTagSerializer


class AbstractTagView(ModelView, ExpertRequiredApiView):
    """
    AbstractTag View
    """

    model = AbstractTag
    form = AbstractTagForm
    serializer = AbstractTagSerializer
    perm_module = "experiences/abstracttag"
    updated_at_attribute_name = "updated_at"

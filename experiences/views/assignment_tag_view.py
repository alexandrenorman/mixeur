# -*- coding: utf-8 -*-
from helpers.views import ExpertRequiredApiView, ModelView

from experiences.models import AssignmentTag
from experiences.forms import AssignmentTagForm
from experiences.serializers import AssignmentTagSerializer


class AssignmentTagView(ModelView, ExpertRequiredApiView):
    """
    AssignmentTag View
    """

    model = AssignmentTag
    form = AssignmentTagForm
    serializer = AssignmentTagSerializer
    perm_module = "experiences/assignmenttag"
    updated_at_attribute_name = "updated_at"

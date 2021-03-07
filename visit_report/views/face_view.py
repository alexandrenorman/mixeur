# -*- coding: utf-8 -*-
from helpers.views import ExpertRequiredApiView, ModelView

from visit_report.models import Face
from visit_report.forms import FaceForm
from visit_report.serializers import FaceSerializer


class FaceView(ModelView, ExpertRequiredApiView):
    """
    Face View
    """

    model = Face
    form = FaceForm
    serializer = FaceSerializer
    perm_module = "face"

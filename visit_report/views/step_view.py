# -*- coding: utf-8 -*-
from helpers.views import ExpertRequiredApiView, ModelView

from visit_report.models import Step
from visit_report.forms import StepForm
from visit_report.serializers import StepSerializer


class StepView(ModelView, ExpertRequiredApiView):
    """
    Step View
    """

    model = Step
    form = StepForm
    serializer = StepSerializer
    perm_module = "step"

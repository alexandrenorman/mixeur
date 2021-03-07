# -*- coding: utf-8 -*-
from helpers.views import ExpertRequiredApiView, ModelView

from visit_report.models import Scenario
from visit_report.forms import ScenarioForm
from visit_report.serializers import ScenarioSerializer


class ScenarioView(ModelView, ExpertRequiredApiView):
    """
    Scenario View
    """

    model = Scenario
    form = ScenarioForm
    serializer = ScenarioSerializer
    perm_module = "scenario"

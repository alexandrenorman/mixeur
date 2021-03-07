# -*- coding: utf-8 -*-
from helpers.views import ExpertRequiredApiView, ModelView

from visit_report.models import ScenarioSummary
from visit_report.forms import ScenarioSummaryForm
from visit_report.serializers import ScenarioSummarySerializer


class ScenarioSummaryView(ModelView, ExpertRequiredApiView):
    """
    ScenarioSummary View
    """

    model = ScenarioSummary
    form = ScenarioSummaryForm
    serializer = ScenarioSummarySerializer
    perm_module = "scenariosummary"

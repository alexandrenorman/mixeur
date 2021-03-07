# -*- coding: utf-8 -*-
from helpers.views import ExpertRequiredApiView, ModelView

from visit_report.models import WorkRecommendation
from visit_report.forms import WorkRecommendationForm
from visit_report.serializers import WorkRecommendationSerializer


class WorkRecommendationView(ModelView, ExpertRequiredApiView):
    """
    WorkRecommendation View
    """

    model = WorkRecommendation
    form = WorkRecommendationForm
    serializer = WorkRecommendationSerializer
    perm_module = "workrecommendation"

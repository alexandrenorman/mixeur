# -*- coding: utf-8 -*-
from helpers.views import ExpertRequiredApiView, ModelView

from visit_report.models import Financing
from visit_report.forms import FinancingForm
from visit_report.serializers import FinancingSerializer


class FinancingView(ModelView, ExpertRequiredApiView):
    """
    Financing View
    """

    model = Financing
    form = FinancingForm
    serializer = FinancingSerializer
    perm_module = "financing"

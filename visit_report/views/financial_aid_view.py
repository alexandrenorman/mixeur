# -*- coding: utf-8 -*-
from helpers.views import ExpertRequiredApiView, ModelView

from visit_report.models import FinancialAid
from visit_report.forms import FinancialAidForm
from visit_report.serializers import FinancialAidSerializer


class FinancialAidView(ModelView, ExpertRequiredApiView):
    """
    FinancialAid View
    """

    model = FinancialAid
    form = FinancialAidForm
    serializer = FinancialAidSerializer
    perm_module = "financialaid"

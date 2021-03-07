# -*- coding: utf-8 -*-
from helpers.views import ExpertRequiredApiView, ModelView

from visit_report.models import Appendix
from visit_report.forms import AppendixForm
from visit_report.serializers import AppendixSerializer


class AppendixView(ModelView, ExpertRequiredApiView):
    """
    Appendix View
    """

    model = Appendix
    form = AppendixForm
    serializer = AppendixSerializer
    perm_module = "appendix"

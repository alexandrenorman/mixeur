# -*- coding: utf-8 -*-
from helpers.views import ExpertRequiredApiView, ModelView

from visit_report.models import System
from visit_report.forms import SystemForm
from visit_report.serializers import SystemSerializer


class SystemView(ModelView, ExpertRequiredApiView):
    """
    System View
    """

    model = System
    form = SystemForm
    serializer = SystemSerializer
    perm_module = "system"

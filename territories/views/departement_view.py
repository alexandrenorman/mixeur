# -*- coding: utf-8 -*-
from helpers.views import ExpertRequiredApiView, ModelView

from territories.models import Departement
from territories.serializers import DepartementSerializer


class DepartementView(ModelView, ExpertRequiredApiView):
    """
    Departement View
    """

    model = Departement
    form = None
    serializer = DepartementSerializer
    perm_module = None

# -*- coding: utf-8 -*-
from helpers.views import ExpertRequiredApiView, ModelView

from territories.models import Epci
from territories.serializers import EpciSerializer


class EpciView(ModelView, ExpertRequiredApiView):
    """
    Epci View
    """

    model = Epci
    form = None
    serializer = EpciSerializer
    perm_module = None

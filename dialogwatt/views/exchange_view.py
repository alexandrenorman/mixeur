# -*- coding: utf-8 -*-
from helpers.views import ExpertRequiredApiView, ModelReadOnlyView

from dialogwatt.models import Exchange
from dialogwatt.serializers import ExchangeSerializer


class ExchangeView(ModelReadOnlyView, ExpertRequiredApiView):
    """
    ExchangeView requires authenticated user
    """

    model = Exchange
    serializer = ExchangeSerializer
    perm_module = "dialogwatt/exchange"

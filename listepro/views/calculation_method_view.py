# -*- coding: utf-8 -*-
from helpers.views import ApiView, ModelView

from listepro.forms import CalculationMethodForm
from listepro.models import CalculationMethod
from listepro.serializers import CalculationMethodSerializer


class CalculationMethodView(ModelView, ApiView):
    """
    CalculationMethod View
    """

    model = CalculationMethod
    form = CalculationMethodForm
    serializer = CalculationMethodSerializer
    perm_module = "listepro/calculationmethod"
    updated_at_attribute_name = "updated_at"

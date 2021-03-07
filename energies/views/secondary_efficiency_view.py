# -*- coding: utf-8 -*-
from helpers.views import ApiView, ModelReadOnlyView

from energies.models import SecondaryEfficiency

from energies.serializers import SecondaryEfficiencySerializer


class SecondaryEfficiencyView(ModelReadOnlyView, ApiView):
    """
    SecondaryEfficiency View
    """

    model = SecondaryEfficiency

    serializer = SecondaryEfficiencySerializer
    perm_module = "energies/secondaryefficiency"
    updated_at_attribute_name = "updated_at"

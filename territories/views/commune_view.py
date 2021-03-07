# -*- coding: utf-8 -*-
from helpers.views import ApiView, ModelReadOnlyView

from territories.models import Commune
from territories.serializers import CommuneSerializer


class CommuneView(ModelReadOnlyView, ApiView):
    """
    Commune View
    """

    model = Commune
    form = None
    serializer = CommuneSerializer
    perm_module = None

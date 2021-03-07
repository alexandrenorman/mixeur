# -*- coding: utf-8 -*-
from helpers.views import ExpertRequiredApiView, ModelView

from territories.models import Region
from territories.serializers import RegionSerializer


class RegionView(ModelView, ExpertRequiredApiView):
    """
    Region View
    """

    model = Region
    form = None
    serializer = RegionSerializer
    perm_module = None

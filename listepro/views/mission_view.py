# -*- coding: utf-8 -*-
from helpers.views import ApiView, ModelView

from listepro.forms import MissionForm
from listepro.models import Mission
from listepro.serializers import MissionSerializer


class MissionView(ModelView, ApiView):
    """
    Mission View
    """

    model = Mission
    form = MissionForm
    serializer = MissionSerializer
    perm_module = "listepro/mission"
    updated_at_attribute_name = "updated_at"

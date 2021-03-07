# -*- coding: utf-8 -*-
from helpers.views import ApiView, ModelView

from listepro.forms import SubMissionForm
from listepro.models import SubMission
from listepro.serializers import SubMissionSerializer


class SubMissionView(ModelView, ApiView):
    """
    SubMission View
    """

    model = SubMission
    form = SubMissionForm
    serializer = SubMissionSerializer
    perm_module = "listepro/submission"
    updated_at_attribute_name = "updated_at"

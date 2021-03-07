# -*- coding: utf-8 -*-
from helpers.views import ApiView, ModelView

from listepro.forms import ActivityForm
from listepro.models import Activity
from listepro.serializers import ActivitySerializer


class ActivityView(ModelView, ApiView):
    """
    Activity View
    """

    model = Activity
    form = ActivityForm
    serializer = ActivitySerializer
    perm_module = "listepro/activity"
    updated_at_attribute_name = "updated_at"

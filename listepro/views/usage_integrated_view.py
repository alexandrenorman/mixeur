# -*- coding: utf-8 -*-
from helpers.views import ApiView, ModelView

from listepro.forms import UsageIntegratedForm
from listepro.models import UsageIntegrated
from listepro.serializers import UsageIntegratedSerializer


class UsageIntegratedView(ModelView, ApiView):
    """
    UsageIntegrated View
    """

    model = UsageIntegrated
    form = UsageIntegratedForm
    serializer = UsageIntegratedSerializer
    perm_module = "listepro/usageintegrated"
    updated_at_attribute_name = "updated_at"

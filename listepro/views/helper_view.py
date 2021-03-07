# -*- coding: utf-8 -*-
from helpers.views import ApiView, ModelView

from listepro.forms import HelperForm
from listepro.models import Helper
from listepro.serializers import HelperSerializer


class HelperView(ModelView, ApiView):
    """
    Helper View
    """

    model = Helper
    form = HelperForm
    serializer = HelperSerializer
    perm_module = "listepro/helper"
    updated_at_attribute_name = "updated_at"

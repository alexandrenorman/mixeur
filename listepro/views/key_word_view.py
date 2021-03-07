# -*- coding: utf-8 -*-
from helpers.views import ApiView, ModelView

from listepro.forms import KeyWordForm
from listepro.models import KeyWord
from listepro.serializers import KeyWordSerializer


class KeyWordView(ModelView, ApiView):
    """
    KeyWord View
    """

    model = KeyWord
    form = KeyWordForm
    serializer = KeyWordSerializer
    perm_module = "listepro/keyword"
    updated_at_attribute_name = "updated_at"

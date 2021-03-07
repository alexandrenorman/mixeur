# -*- coding: utf-8 -*-
from helpers.views import ApiView, ModelView

from listepro.forms import KeyWordCategoryForm
from listepro.models import KeyWordCategory
from listepro.serializers import KeyWordCategorySerializer


class KeyWordCategoryView(ModelView, ApiView):
    """
    KeyWordCategory View
    """

    model = KeyWordCategory
    form = KeyWordCategoryForm
    serializer = KeyWordCategorySerializer
    perm_module = "listepro/keywordcategory"
    updated_at_attribute_name = "updated_at"

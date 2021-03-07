# -*- coding: utf-8 -*-
from helpers.views import ExpertRequiredApiView, ModelReadOnlyView

from fac.models import TypeValorization
from fac.serializers import TypeValorizationSerializer


class TypeValorizationView(ModelReadOnlyView, ExpertRequiredApiView):
    """
    TypeValorization View
    """

    model = TypeValorization
    serializer = TypeValorizationSerializer
    perm_module = "typevalorization"
    updated_at_attribute_name = "updated_at"

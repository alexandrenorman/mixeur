# -*- coding: utf-8 -*-
from fac.forms import ContactsDuplicateForm
from fac.models import ContactsDuplicate
from fac.serializers import ContactsDuplicateSerializer

from helpers.views import ExpertRequiredApiView, ModelView


class ContactsDuplicateView(ModelView, ExpertRequiredApiView):
    """
    ContactsDuplicate View
    """

    model = ContactsDuplicate
    form = ContactsDuplicateForm
    serializer = ContactsDuplicateSerializer
    perm_module = "fac/contactsduplicate"

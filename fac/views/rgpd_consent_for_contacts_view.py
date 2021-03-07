# -*- coding: utf-8 -*-
from helpers.views import ExpertRequiredApiView, ModelView

from fac.models import RgpdConsentForContacts
from fac.forms import RgpdConsentForContactsForm
from fac.serializers import RgpdConsentForContactsSerializer


class RgpdConsentForContactsView(ModelView, ExpertRequiredApiView):
    """
    RgpdConsentForContacts View
    """

    model = RgpdConsentForContacts
    form = RgpdConsentForContactsForm
    serializer = RgpdConsentForContactsSerializer
    perm_module = "rgpdconsentforcontacts"

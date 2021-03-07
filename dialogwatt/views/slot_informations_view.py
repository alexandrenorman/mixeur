# -*- coding: utf-8 -*-
from helpers.views import ApiView, ModelReadOnlyView
from dialogwatt.models import Slot


from dialogwatt.forms import SlotForm
from dialogwatt.serializers import SlotInformationsSerializer


class SlotInformationsView(ModelReadOnlyView, ApiView):
    """
    Return extensive informations about place, group and advisors for a slot
    """

    model = Slot
    form = SlotForm
    serializer = SlotInformationsSerializer
    perm_module = "dialogwatt/slot_informations"

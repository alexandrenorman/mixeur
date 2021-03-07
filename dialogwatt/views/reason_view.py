# -*- coding: utf-8 -*-
from datetime import datetime

from dialogwatt.forms import ReasonForm
from dialogwatt.models import Reason, Slot
from dialogwatt.serializers import ReasonSerializer

from helpers.views import ApiView, ModelView


class ReasonView(ModelView, ApiView):
    """
    ReasonView requires authenticated user

    get :model:`dialogwatt.Reason`

    """

    model = Reason
    form = ReasonForm
    serializer = ReasonSerializer
    perm_module = "dialogwatt/reason"

    def filter(self, request, queryset):  # NOQA: A003
        if "place" in request.GET:
            filtered_reasons = Slot.active_and_future.filter(
                start_date__date__gte=datetime.today(),
                place__exact=request.GET["place"],
            ).values("reasons")

            queryset = queryset.filter(pk__in=filtered_reasons)

        return queryset

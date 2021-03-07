# -*- coding: utf-8 -*-
from helpers.views import ApiView, ModelView

from listepro.forms import SegmentForm
from listepro.models import Segment
from listepro.serializers import SegmentSerializer


class SegmentView(ModelView, ApiView):
    """
    Segment View
    """

    model = Segment
    form = SegmentForm
    serializer = SegmentSerializer
    perm_module = "listepro/segment"
    updated_at_attribute_name = "updated_at"

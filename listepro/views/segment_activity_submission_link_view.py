# -*- coding: utf-8 -*-
from helpers.views import ApiView, ModelView

from listepro.forms import SegmentActivitySubMissionLinkForm
from listepro.models import SegmentActivitySubMissionLink
from listepro.serializers import SegmentActivitySubMissionLinkSerializer


class SegmentActivitySubMissionLinkView(ModelView, ApiView):
    """
    SegmentActivitySubMissionLink View
    """

    def filter(self, request, queryset):  # NOQA: A003
        """
        Filter queryset from request argument
        """

        queryset = (
            queryset.prefetch_related("segment")
            .prefetch_related("activity")
            .prefetch_related("sub_mission")
        )

        return queryset

    model = SegmentActivitySubMissionLink
    form = SegmentActivitySubMissionLinkForm
    serializer = SegmentActivitySubMissionLinkSerializer
    perm_module = "listepro/segmentactivitysubmissionlink"
    updated_at_attribute_name = "updated_at"

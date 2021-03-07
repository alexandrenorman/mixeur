# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _

from core.models import MixeurBaseModel

from .activity import Activity
from .segment import Segment
from .sub_mission import SubMission


class SegmentActivitySubMissionLink(MixeurBaseModel):
    class Meta:
        verbose_name = _("Lien segment/activité/sous-missions")
        verbose_name_plural = _("Liens segment/activité/sous-missions")

    segment = models.ForeignKey(Segment, on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    sub_mission = models.ForeignKey(SubMission, on_delete=models.CASCADE)

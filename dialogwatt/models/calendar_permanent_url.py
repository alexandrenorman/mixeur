# -*- coding: utf-8 -*-
import uuid
from django.db import models

from django.utils.translation import ugettext_lazy as _
from core.models import MixeurBaseModel

from accounts.models import User
from .place import Place
from .reason import Reason


class CalendarPermanentUrl(MixeurBaseModel):
    class Meta:
        verbose_name = _("Filtrages permanents de calendrier")

    user = models.ForeignKey(
        User,
        verbose_name=_("Conseiller"),
        limit_choices_to=models.Q(user_type="advisor")
        | models.Q(user_type="superadvisor"),
        on_delete=models.CASCADE,
        null=False,
        related_name="calendar",
    )

    unique_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    places = models.ManyToManyField(Place, verbose_name=_("Lieux d'accueil"))
    reasons = models.ManyToManyField(Reason, verbose_name=_("Motifs de rdv"))
    advisors = models.ManyToManyField(User, verbose_name=_("Conseillers"))

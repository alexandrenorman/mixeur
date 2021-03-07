# -*- coding: utf-8 -*-
import uuid
from django.db import models
from django.contrib.postgres.fields import JSONField
from core.models import MixeurBaseModel

from django.utils.translation import ugettext_lazy as _

from django.core.serializers.json import DjangoJSONEncoder


class PdfTempStore(MixeurBaseModel):
    class Meta:
        verbose_name = _("Pdf Temporary Store")

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    data = JSONField(encoder=DjangoJSONEncoder, blank=True)

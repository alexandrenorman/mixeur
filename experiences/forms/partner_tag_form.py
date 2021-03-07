# -*- coding: utf-8 -*-
from experiences.forms import AbstractTagForm
from experiences.models import PartnerTag


class PartnerTagForm(AbstractTagForm):
    class Meta:
        model = PartnerTag
        exclude = ["created_at", "updated_at"]

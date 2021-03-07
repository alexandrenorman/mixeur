# -*- coding: utf-8 -*-
from experiences.forms import AbstractTagForm
from experiences.models import PublicTag


class PublicTagForm(AbstractTagForm):
    class Meta:
        model = PublicTag
        exclude = ["created_at", "updated_at"]

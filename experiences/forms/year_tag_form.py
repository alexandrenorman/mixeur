# -*- coding: utf-8 -*-
from experiences.forms import AbstractTagForm
from experiences.models import YearTag


class YearTagForm(AbstractTagForm):
    class Meta:
        model = YearTag
        exclude = ["created_at", "updated_at"]

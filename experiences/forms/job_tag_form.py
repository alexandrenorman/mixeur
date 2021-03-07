# -*- coding: utf-8 -*-
from experiences.forms import AbstractTagForm
from experiences.models import JobTag


class JobTagForm(AbstractTagForm):
    class Meta:
        model = JobTag
        exclude = ["created_at", "updated_at"]

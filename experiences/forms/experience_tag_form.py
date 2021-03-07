# -*- coding: utf-8 -*-
from experiences.forms import AbstractTagForm
from experiences.models import ExperienceTag


class ExperienceTagForm(AbstractTagForm):
    class Meta:
        model = ExperienceTag
        exclude = ["created_at", "updated_at"]

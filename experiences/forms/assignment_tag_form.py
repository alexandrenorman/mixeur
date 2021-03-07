# -*- coding: utf-8 -*-
from experiences.forms import AbstractTagForm
from experiences.models import AssignmentTag


class AssignmentTagForm(AbstractTagForm):
    class Meta:
        model = AssignmentTag
        exclude = ["created_at", "updated_at"]

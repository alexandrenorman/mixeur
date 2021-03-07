# -*- coding: utf-8 -*-
from django.contrib.contenttypes.admin import GenericTabularInline

from fac.models import Note


class NoteInline(GenericTabularInline):
    model = Note
    extra = 0
    exclude = []
    readonly_fields = ["linked_object"]
    show_change_link = True

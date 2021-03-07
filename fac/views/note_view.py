# -*- coding: utf-8 -*-
from django.contrib.contenttypes.models import ContentType
from fac.forms import NoteForm
from fac.models import Note, Tag
from fac.serializers import NoteSerializer
from helpers.views import ExpertRequiredApiView, ModelView

from .reminder_view import ReminderViewMixin


class NoteView(ReminderViewMixin, ModelView, ExpertRequiredApiView):
    """
    Note View
    """

    model = Note
    form = NoteForm
    serializer = NoteSerializer
    perm_module = "note"

    def post_save(self, request, note, data, created):
        super().post_save(request, note, data, created)
        self._save_m2m_from_select(
            instance=note,
            attribute="tags",
            model_queryset=Tag.objects,
            data=data.get("tags", []),
        )

        if self.request.method == "POST":
            note.creator = self.request.user
            note.save()

    def filter(self, request, queryset):
        note_type = request.GET.get("type")
        object_id = request.GET.get("object_id")

        if not note_type or not object_id:
            return queryset

        if note_type != "contact" and note_type != "organization":
            return queryset

        content_type = ContentType.objects.get(app_label="fac", model=note_type)
        return (
            queryset.filter(object_id=object_id, content_type=content_type)
            .accessible_by(request.user)
            .prefetch_related("creator", "tags", "owning_group")
        )

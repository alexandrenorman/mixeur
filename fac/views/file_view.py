# -*- coding: utf-8 -*-
import io
import os.path
import zipfile

from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse

from fac.forms import FileForm
from fac.models import File, Tag
from fac.serializers import FileSerializer
from helpers.views import ExpertRequiredApiView, ModelView


class FileView(ModelView, ExpertRequiredApiView):
    """
    File View
    """

    model = File
    form = FileForm
    serializer = FileSerializer
    perm_module = "file"

    def post_save(self, request, file, file_data, created):
        self._save_m2m_from_select(
            instance=file,
            attribute="tags",
            model_queryset=Tag.objects,
            data=file_data.get("tags", []),
        )

    def filter(self, request, queryset):
        file_type = request.GET.get("linkedObjectType")
        object_id = request.GET.get("objectId")
        if not file_type or not object_id:
            return queryset

        if file_type != "contact" and file_type != "organization":
            return queryset

        content_type = ContentType.objects.get(app_label="fac", model=file_type)
        return queryset.filter(object_id=object_id, content_type=content_type)

    def list(self, request, *args, **kwargs):
        if request.GET.get("zip") != "1":
            return super().list(request, *args, **kwargs)

        allowed_groups = {
            group.pk for group in request.user.group.laureate_groups.all()
        }
        allowed_groups.add(request.user.group.pk)

        asked_pks = [int(pk) for pk in request.GET["files"].split(",")]
        files = File.objects.filter(pk__in=asked_pks)
        files = files.filter(owning_group__in=allowed_groups)

        in_memory_file = io.BytesIO()
        with zipfile.ZipFile(in_memory_file, "w", zipfile.ZIP_DEFLATED) as files_zipped:
            for f in files:
                if not f.document or not f.document.path:
                    continue
                files_zipped.write(
                    f.document.path, arcname=os.path.basename(f.document.path)
                )
        in_memory_file.seek(0)

        response = HttpResponse(
            content=in_memory_file.read(), content_type="application/zip"
        )

        response["Content-Disposition"] = "attachment; filename=files.zip"

        return response

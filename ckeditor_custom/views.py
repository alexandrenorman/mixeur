# -*- coding: utf-8 -*-
from helpers.views import ExpertRequiredApiView

import json
import os
from django.http import JsonResponse
import urllib.parse


from helpers.helpers import decode_base64_file, unique_filename_in_path


from config.settings import MEDIA_ROOT, MEDIA_URL

# https://github.com/django-ckeditor/django-ckeditor/blob/master/ckeditor_uploader/views.py


class CkEditorUpload(ExpertRequiredApiView):
    def post(self, request, *args, **kwargs):
        json_data = json.loads(request.body)

        filename = json_data["filename"]
        picfile = decode_base64_file(json_data["file"]).read()

        try:
            group_pk = request.user.group.pk
        except AttributeError:
            group_pk = "anonymous"

        dir_path = os.path.join(MEDIA_ROOT, "ckeditor_uploaded", str(group_pk))
        partial_path = urllib.parse.urljoin(MEDIA_URL, f"ckeditor_uploaded/{group_pk}/")

        if not os.path.isdir(dir_path):
            os.makedirs(dir_path)

        valid_filename = unique_filename_in_path(dir_path, filename)

        path = os.path.join(dir_path, valid_filename)

        with open(path, "wb") as fpic:
            fpic.write(picfile)

        url = urllib.parse.urljoin(partial_path, valid_filename)

        retdata = {"url": url, "uploaded": "1", "fileName": valid_filename}
        return JsonResponse(retdata, safe=False)

# -*- coding: utf-8 -*-
from helpers.views import ExpertRequiredApiView, ModelView

from fac.models import FileImport
from fac.forms import FileImportForm
from fac.serializers import FileImportSerializer


class FileImportView(ModelView, ExpertRequiredApiView):
    """
    FileImport View
    """

    model = FileImport
    form = FileImportForm
    serializer = FileImportSerializer
    perm_module = "fileimport"

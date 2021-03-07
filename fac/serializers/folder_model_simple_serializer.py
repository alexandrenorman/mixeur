# -*- coding: utf-8 -*-
from fac.models import FolderModel
from helpers.serializers import AutoModelSerializer


class FolderModelSimpleSerializer(AutoModelSerializer):
    model = FolderModel
    exclude = ["project", "icon_marker"]

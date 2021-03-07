# -*- coding: utf-8 -*-
from helpers.views import ExpertRequiredApiView, ModelView

from newsletters.models import Image
from newsletters.forms import ImageForm
from newsletters.serializers import ImageSerializer


class ImageView(ModelView, ExpertRequiredApiView):
    """
    Image View
    """

    model = Image
    form = ImageForm
    serializer = ImageSerializer
    perm_module = "newsletters/image"

# -*- coding: utf-8 -*-
from helpers.helpers import decode_base64_file
from helpers.views import ApiView, ModelView

from listepro.forms import ProfessionalImageForm
from listepro.models import ProfessionalImage
from listepro.serializers import ProfessionalImageSerializer


class ProfessionalImageView(ModelView, ApiView):
    """
    ProfessionalImage View
    """

    model = ProfessionalImage
    form = ProfessionalImageForm
    serializer = ProfessionalImageSerializer
    perm_module = "listepro/professionalimage"
    updated_at_attribute_name = "updated_at"

    def filter(self, request, queryset):  # NOQA: A003
        """
        Filter queryset from request argument
        """
        pro = request.GET.get("production")

        if pro:
            queryset = queryset.filter(production=pro)

        queryset = queryset.prefetch_related("production")

        return queryset

    def post_save(self, request, instance, image_data, created):

        instance.cropped = decode_base64_file(image_data["cropped"])

        if "cropped" in image_data:
            if image_data["cropped"] is None:
                instance.cropped = None
            else:
                instance.cropped = decode_base64_file(image_data["cropped"])

            instance.save()

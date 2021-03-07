# -*- coding: utf-8 -*-

from django.http import JsonResponse

from custom_forms.models import CustomForm

from helpers.views import ExpertRequiredApiView


class CustomFormLastUpdateView(ExpertRequiredApiView):
    """
    CustomView requires authenticated user
    """

    def get(self, request, *args, **kwargs):
        """
        return last update of CustomForm
        """
        if CustomForm.objects.all().exists():
            last_update = (
                CustomForm.objects.all().order_by("-updated_at").first().updated_at
            )
        else:
            last_update = 0
        return JsonResponse(
            {
                "last_update": last_update,
            }
        )

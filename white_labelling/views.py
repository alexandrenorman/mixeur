# -*- coding: utf-8 -*-
from django.http import JsonResponse

from helpers.views import ApiView


from .models import WhiteLabelling

from .serializers import WhiteLabellingSerializer


class WhiteLabellingView(ApiView):
    def default(self):
        return (
            WhiteLabelling.objects.filter(is_default=True).first()
            or WhiteLabelling.objects.first()
        )

    def get(self, request, *args, **kwargs):
        domain = kwargs.get("domain")

        wl = WhiteLabelling.objects.filter(domain=domain).first() or self.default()

        if not wl:
            return JsonResponse({"error": "No WhiteLabelling defined"})

        serializer = WhiteLabellingSerializer(wl)
        return JsonResponse(serializer.data)

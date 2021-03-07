from django.views import View
from django.http import JsonResponse
from django.conf import settings


class AppInfosView(View):
    def get(self, request, *args, **kwargs):
        return JsonResponse({"version": settings.APP_VERSION})

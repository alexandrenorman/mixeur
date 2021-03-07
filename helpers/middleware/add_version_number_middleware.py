# -*- coding: utf-8 -*-

from config.settings import APP_VERSION


class AddVersionNumberMiddleware:
    """
    Add a response header "x-server-version" on json
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response["x-server-version"] = APP_VERSION
        return response

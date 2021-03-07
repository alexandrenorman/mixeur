# -*- coding: utf-8 -*-

import simplejson
from helpers.json import (
    camel_to_snakecase,
    snakecase_to_camel,
    change_dict_naming_convention,
)


class TransformPropertiesCaseMiddleware:
    """
    Convert a json request to /api/ back and forth CamelCase / snake_case

    can be avoided if passing "Properties-Case-Transform: no" in request header
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        if (
            "Properties-Case-Transform" in request.headers
            and request.headers["Properties-Case-Transform"] == "no"
        ):
            response = self.get_response(request)
            return response

        if request.content_type in ["application/json"] and request.path.startswith(
            "/api/"
        ):
            # See https://stackoverflow.com/questions/22740310/how-to-update-django-httprequest-body-in-middleware
            if request.body:
                try:
                    data = simplejson.loads(
                        getattr(request, "_body", request.body).decode("utf-8")
                    )
                    assert isinstance(data, dict)
                except (ValueError, AssertionError):
                    response = self.get_response(request)
                    return response

                converted_data = change_dict_naming_convention(data, camel_to_snakecase)
                request._body = simplejson.dumps(converted_data).encode("utf-8")

            # Get response
            response = self.get_response(request)

            # Code to be executed for each request/response after
            # the view is called.

            if response._headers["content-type"][1] == "application/json":
                try:
                    data = simplejson.loads(response.content)
                    assert isinstance(data, dict) or isinstance(data, list)
                except (ValueError, AssertionError):
                    response = self.get_response(request)
                    return response

                converted_data = change_dict_naming_convention(data, snakecase_to_camel)
                response.content = simplejson.dumps(converted_data)

        else:
            response = self.get_response(request)

        return response

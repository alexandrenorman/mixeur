# -*- coding: utf-8 -*-
from rest_framework.response import Response
from rest_framework import status

from rest_framework_jwt.views import ObtainJSONWebToken

from django.utils import timezone

from accounts.models import LogUser
from white_labelling.models import WhiteLabelling


class CustomObtainJSONWebToken(ObtainJSONWebToken):
    def post(self, request, *args, **kwargs):
        # email is lower case !
        try:
            request.data["email"] = request.data["email"].lower()
        except Exception:
            pass

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.object.get("user")

            user.last_login = timezone.now()
            user.save()

            try:
                wl = WhiteLabelling.objects.get(domain=request._request.get_host())
            except Exception:
                wl = None

            LogUser.objects.create(user=user, white_labelling=wl)
            if not user.can_login:
                return Response(
                    {"error": "structure inactive"}, status=status.HTTP_400_BAD_REQUEST
                )

        return super().post(request, *args, **kwargs)

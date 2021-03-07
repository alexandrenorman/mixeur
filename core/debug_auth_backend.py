from django.contrib.auth.backends import ModelBackend
from accounts.models import User


class DebugAuthBackend(ModelBackend):
    """
    Authenticate user with any password used in DEBUG_MODE
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is not None:
            try:
                user = User.objects.get(email=username)
            except User.DoesNotExist:
                return None

        else:
            try:
                user = User.objects.get(email=kwargs["email"])
            except User.DoesNotExist:
                return None

        return user

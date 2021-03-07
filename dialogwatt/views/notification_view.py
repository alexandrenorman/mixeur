# -*- coding: utf-8 -*-
from helpers.views import ExpertRequiredApiView, ModelView

from dialogwatt.models import Reason, Place
from dialogwatt.models import Notification
from dialogwatt.forms import NotificationForm
from dialogwatt.serializers import NotificationSerializer

from accounts.models import User


class NotificationView(ModelView, ExpertRequiredApiView):
    """
    NotificationView requires authenticated user
    """

    model = Notification
    form = NotificationForm
    serializer = NotificationSerializer
    perm_module = "dialogwatt/notification"

    def post_save(self, request, notification, notification_data, created):
        for m2m in [
            {"attribute": "reasons", "qs": Reason.objects, "data": "reasons"},
            {"attribute": "places", "qs": Place.objects, "data": "places"},
            {"attribute": "advisors", "qs": User.advisors, "data": "advisors"},
        ]:
            self._save_m2m_from_pk(
                instance=notification,
                attribute=m2m["attribute"],
                model_queryset=m2m["qs"],
                pks=notification_data[m2m["data"]],
            )

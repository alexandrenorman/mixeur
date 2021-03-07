# -*- coding: utf-8 -*-
from django.db import models
from helpers.views import ModelView
import datetime


class RecordableModelMixin(models.Model):
    """
    """

    class Meta:
        abstract = True

    history = models.TextField(verbose_name="Historique des modifications", default="")


class RecordableViewMixin(ModelView):
    """
    """

    class Meta:
        abstract = True

    def post_save(self, request, instance, instance_data, created):
        """
        """
        date = datetime.datetime.now().replace(microsecond=0).isoformat()

        if created:
            instance.history = (
                instance.history
                + f"- Creation: {request.user.full_name} ({request.user.email}) - {date}\n"
            )
        else:
            instance.history = (
                instance.history
                + f"- Modification: {request.user.full_name} ({request.user.email}) - {date}\n"
            )

        instance.save()

# -*- coding: utf-8 -*-
from helpers.views import ApiView, ModelView

from listepro.forms import JobForm
from listepro.models import Job
from listepro.serializers import JobSerializer


class JobView(ModelView, ApiView):
    """
    Job View
    """

    model = Job
    form = JobForm
    serializer = JobSerializer
    perm_module = "listepro/job"
    updated_at_attribute_name = "updated_at"

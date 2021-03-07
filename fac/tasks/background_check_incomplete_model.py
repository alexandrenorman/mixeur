# -*- coding: utf-8 -*-
import logging

from background_task import background

from django.apps import apps

from fac.models import IncompleteModel

logger = logging.getLogger(__name__)  # NOQA


@background(schedule=10)
def background_check_incomplete_model(app_label, model_name, pk):
    logger.warning(
        f"Launch background check incomplete model {app_label}/{model_name}/{pk}"
    )

    model = apps.get_model(app_label=app_label, model_name=model_name)
    try:
        obj = model.objects.get(pk=pk)
    except Exception as error:
        logger.error(
            f"Error background check incomplete model {app_label}/{model_name}/{pk} -- {error}"
        )
    else:
        if IncompleteModel.check_incomplete_model_and_save(obj):
            logger.warning(
                f"Background check incomplete model {app_label}/{model_name}/{pk} -> incomplete fields"
            )

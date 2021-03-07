# -*- coding: utf-8 -*-
from django.apps import AppConfig
from django.db.utils import ProgrammingError

from core.helpers import is_jenkins_build

from .helpers import generate_traefik_configuration


class WhiteLabellingConfig(AppConfig):
    name = "white_labelling"

    def ready(self):
        if not is_jenkins_build():
            try:
                generate_traefik_configuration()
            except ProgrammingError:
                pass

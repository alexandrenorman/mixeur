# -*- coding: utf-8 -*-
from django.db import models

from .abstract_tag import AbstractTag


class PartnerTag(AbstractTag):
    is_european = models.BooleanField("partenaire européen ?", default=False)

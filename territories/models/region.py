# -*- coding: utf-8 -*-
from django.db import models

from djgeojson.fields import PointField
from core.models import MixeurBaseModel


class Region(MixeurBaseModel):
    class Meta:
        ordering = ("name",)

    name = models.CharField(max_length=256)
    inseecode = models.CharField(max_length=8, unique=True)
    geom = PointField()

    def __str__(self):
        return self.name

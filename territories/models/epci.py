# -*- coding: utf-8 -*-
from django.db import models

from djgeojson.fields import PointField
from core.models import MixeurBaseModel


class EpciQuerySet(models.QuerySet):
    def dict_list(self):
        return [{"id": item.id, "name": item.name} for item in self]


class EpciManager(models.Manager):
    def get_queryset(self):
        return EpciQuerySet(self.model, using=self._db)


class Epci(MixeurBaseModel):
    class Meta:
        ordering = ("name",)

    name = models.CharField(max_length=256)
    inseecode = models.CharField(max_length=9, unique=True)
    geom = PointField()

    objects = EpciManager()

    def __str__(self):
        return self.name

# -*- coding: utf-8 -*-
from django.db import models

from djgeojson.fields import PointField

from .region import Region
from core.models import MixeurBaseModel


class DepartementQuerySet(models.QuerySet):
    def dict_list(self):
        return [{"id": item.id, "name": str(item)} for item in self]


class DepartementManager(models.Manager):
    def get_queryset(self):
        return DepartementQuerySet(self.model, using=self._db)


class Departement(MixeurBaseModel):
    class Meta:
        ordering = ("name",)

    name = models.CharField(max_length=256)
    inseecode = models.CharField(max_length=8, unique=True)
    geom = PointField()
    region = models.ForeignKey(Region, on_delete=models.CASCADE)

    objects = DepartementManager()

    def __str__(self):
        return f"{self.inseecode} - {self.name}"

# -*- coding: utf-8 -*-
from django.db import models

from djgeojson.fields import PointField

from .epci import Epci
from .departement import Departement
from core.models import MixeurBaseModel


class CommuneQuerySet(models.QuerySet):
    def dict_list(self):
        return [{"id": item.id, "name": item.rich_name} for item in self]


class CommuneManager(models.Manager):
    def get_queryset(self):
        return CommuneQuerySet(self.model, using=self._db)


class Commune(MixeurBaseModel):
    class Meta:
        ordering = ("name",)

    name = models.CharField(max_length=256)
    postcode = models.CharField(max_length=8, blank=True)
    inseecode = models.CharField(max_length=8, unique=True)
    departement = models.ForeignKey(Departement, on_delete=models.CASCADE)
    epci = models.ForeignKey(Epci, blank=True, null=True, on_delete=models.CASCADE)
    geom = PointField()

    objects = CommuneManager()

    @property
    def rich_name(self):
        to_return = ""
        if self.epci:
            to_return += f"{self.epci} - "
        to_return += f"{self.inseecode} - "

        to_return += f"{self.name}"

        return to_return

    def __str__(self):
        return self.rich_name

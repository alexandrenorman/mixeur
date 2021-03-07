# -*- coding: utf-8 -*-
import pytz
from django.utils import timezone
from django.db import models

from django.utils.translation import ugettext_lazy as _
from core.models import MixeurBaseModel
import datetime

from django.contrib.postgres.fields import JSONField

from .group_of_newsletters import GroupOfNewsletters, DEFAULT_GRAPHIC_CHARTER


class NewsletterQueryset(models.QuerySet):
    def accessible_by(self, user):
        if user.is_administrator:
            return self

        return self.filter(group_of_newsletters__group=user.group)


class NewsletterManager(models.Manager.from_queryset(NewsletterQueryset)):
    """
    """

    def valid(self):
        return self.filter(fileimport=None)

    def being_imported(self):
        return self.exclude(fileimport=None)


def PLUGINS():
    return {"data": []}


class Newsletter(MixeurBaseModel):
    class Meta:
        verbose_name = _("Newsletter")
        unique_together = ("group_of_newsletters", "slug")

    objects = NewsletterManager()

    group_of_newsletters = models.ForeignKey(
        GroupOfNewsletters,
        verbose_name=_("Groupe de newsletters"),
        on_delete=models.CASCADE,
    )
    slug = models.SlugField(_("Slug"), unique=False)
    title = models.CharField(
        verbose_name=_("Titre"), blank=False, null=False, max_length=100
    )
    is_active = models.BooleanField(verbose_name=_("Est publiée ?"), default=True)
    is_public = models.BooleanField(verbose_name=_("Est publique ?"), default=True)
    publication_start_date = models.DateTimeField(
        _("Date et heure de début de publication"), default=timezone.now
    )
    publication_end_date = models.DateTimeField(
        _("Date et heure de fin de publication"), blank=True, null=True
    )

    # header
    # footer
    # palette

    description = models.TextField(verbose_name=_("Description"), blank=True, null=True)

    graphic_charter = JSONField(
        verbose_name=_("Charte graphique"), default=DEFAULT_GRAPHIC_CHARTER
    )
    plugins = JSONField(verbose_name=_("Liste des plugins"), default=PLUGINS)

    @property
    def is_published(self):
        now = datetime.datetime.now().astimezone(pytz.timezone("Europe/Paris"))
        return (
            self.group_of_newsletters.is_active
            and self.group_of_newsletters.is_public
            and self.is_active
            and self.is_public
            and (
                self.publication_start_date is None
                or now >= self.publication_start_date
            )
            and (self.publication_end_date is None or self.publication_end_date < now)
        )

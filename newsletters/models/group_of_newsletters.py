# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.postgres.fields import JSONField

from django.utils.translation import ugettext_lazy as _
from core.models import MixeurBaseModel


class GroupOfNewslettersQueryset(models.QuerySet):
    def accessible_by(self, user):
        if user.is_administrator:
            return self

        return self.filter(group=user.group)


class GroupOfNewslettersManager(
    models.Manager.from_queryset(GroupOfNewslettersQueryset)
):
    """
    """

    def valid(self):
        return self.filter(fileimport=None)

    def being_imported(self):
        return self.exclude(fileimport=None)


def DEFAULT_GRAPHIC_CHARTER():
    return {
        "body": {
            "width": 800,
            "fontSize": 12,
            "color": "#333",
            "backgroundColor": "#fff",
            "outerBackgroundColor": "#fff",
        },
        "h1": {"color": "#9a258f", "backgroundColor": "#fff", "fontSize": 20},
        "h2": {"color": "#ffcc00", "backgroundColor": "#fff", "fontSize": 20},
        "h3": {"color": "#888", "backgroundColor": "#fff", "fontSize": 15},
        "link": {"color": "#9a258f"},
        "hr": {"color": "#9a258f", "size": 2},
        "extraCss": "",
    }


def gon_directory_path(instance, slot, filename):
    return "group_of_newsletters/{0}/{1}/{2}".format(instance.pk, slot, filename)


def header_path(instance, filename):
    return gon_directory_path(instance, "header", filename)


def footer_path(instance, filename):
    return gon_directory_path(instance, "footer", filename)


class GroupOfNewsletters(MixeurBaseModel):
    class Meta:
        verbose_name = _("Groupe de newsletters")
        unique_together = ("group", "slug")

    objects = GroupOfNewslettersManager()

    group = models.ForeignKey(
        "accounts.group", verbose_name=_("Structure"), on_delete=models.CASCADE
    )
    slug = models.SlugField(_("Slug"), unique=False)
    title = models.CharField(
        verbose_name=_("Titre"), blank=False, null=False, max_length=100
    )
    is_active = models.BooleanField(verbose_name=_("Est publié ?"), default=True)
    is_public = models.BooleanField(verbose_name=_("Est public ?"), default=True)

    header = models.ImageField(
        verbose_name="Image d'entête", upload_to=header_path, blank=True, null=True
    )
    header_link = models.URLField(_("Url"), blank=True, null=True)

    footer = models.ImageField(
        verbose_name="Image de pied", upload_to=footer_path, blank=True, null=True
    )
    footer_link = models.URLField(_("Url"), blank=True, null=True)

    description = models.TextField(verbose_name=_("Description"), blank=True, null=True)

    graphic_charter = JSONField(
        verbose_name=_("Charte graphique"), default=DEFAULT_GRAPHIC_CHARTER
    )

    @property
    def updated_at_including_newsletters(self):
        if self.newsletter_set.exists():
            return max(
                self.updated_at, max([x.updated_at for x in self.newsletter_set.all()])
            )
        else:
            return self.updated_at

    @property
    def has_published_newsletters(self):
        for newsletter in self.newsletter_set.all():
            if newsletter.is_published:
                return True

        return False

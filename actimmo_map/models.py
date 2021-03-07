# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _

from phonenumber_field.modelfields import PhoneNumberField

from core.models import MixeurBaseModel


def group_directory_path(instance, filename):
    return "actimmo_map/groups/{0}/{1}".format(instance.id, filename)


class ActimmoMap(MixeurBaseModel):
    class Meta:
        verbose_name = _("Carte de progression du projet Actimmo")
        verbose_name_plural = _("Carte de progression du projet Actimmo")

    DEPARTMENT = (
        ("01", "Ain"),
        ("02", "Aisne"),
        ("03", "Allier"),
        ("04", "Alpes-de-Haute-Provence"),
        ("05", "Hautes-Alpes"),
        ("06", "Alpes-Maritimes"),
        ("07", "Ardèche"),
        ("08", "Ardennes"),
        ("09", "Ariège"),
        ("10", "Aube"),
        ("11", "Aude"),
        ("12", "Aveyron"),
        ("13", "Bouches-du-Rhône"),
        ("14", "Calvados"),
        ("15", "Cantal"),
        ("16", "Charente"),
        ("17", "Charente-Maritime"),
        ("18", "Cher"),
        ("19", "Corrèze"),
        ("21", "Côte-d'Or"),
        ("22", "Côtes-d'Armor"),
        ("23", "Creuse"),
        ("24", "Dordogne"),
        ("25", "Doubs"),
        ("26", "Drôme"),
        ("27", "Eure"),
        ("28", "Eure-et-Loir"),
        ("29", "Finistère"),
        ("2A", "Corse-du-Sud"),
        ("2B", "Haute-Corse"),
        ("30", "Gard"),
        ("31", "Haute-Garonne"),
        ("32", "Gers"),
        ("33", "Gironde"),
        ("34", "Hérault"),
        ("35", "Ille-et-Vilaine"),
        ("36", "Indre"),
        ("37", "Indre-et-Loire"),
        ("38", "Isère"),
        ("39", "Jura"),
        ("40", "Landes"),
        ("41", "Loir-et-Cher"),
        ("42", "Loire"),
        ("43", "Haute-Loire"),
        ("44", "Loire-Atlantique"),
        ("45", "Loiret"),
        ("46", "Lot"),
        ("47", "Lot-et-Garonne"),
        ("48", "Lozère"),
        ("49", "Maine-et-Loire"),
        ("50", "Manche"),
        ("51", "Marne"),
        ("52", "Haute-Marne"),
        ("53", "Mayenne"),
        ("54", "Meurthe-et-Moselle"),
        ("55", "Meuse"),
        ("56", "Morbihan"),
        ("57", "Moselle"),
        ("58", "Nièvre"),
        ("59", "Nord"),
        ("60", "Oise"),
        ("61", "Orne"),
        ("62", "Pas-de-Calais"),
        ("63", "Puy-de-Dôme"),
        ("64", "Pyrénées-Atlantiques"),
        ("65", "Hautes-Pyrénées"),
        ("66", "Pyrénées-Orientales"),
        ("67", "Bas-Rhin"),
        ("68", "Haut-Rhin"),
        ("69", "Rhône"),
        ("70", "Haute-Saône"),
        ("71", "Saône-et-Loire"),
        ("72", "Sarthe"),
        ("73", "Savoie"),
        ("74", "Haute-Savoie"),
        ("75", "Paris"),
        ("76", "Seine-Maritime"),
        ("77", "Seine-et-Marne"),
        ("78", "Yvelines"),
        ("79", "Deux-Sèvres"),
        ("80", "Somme"),
        ("81", "Tarn"),
        ("82", "Tarn-et-Garonne"),
        ("83", "Var"),
        ("84", "Vaucluse"),
        ("85", "Vendée"),
        ("86", "Vienne"),
        ("87", "Haute-Vienne"),
        ("88", "Vosges"),
        ("89", "Yonne"),
        ("90", "Territoire de Belfort"),
        ("91", "Essonne"),
        ("92", "Hauts-de-Seine"),
        ("93", "Seine-Saint-Denis"),
        ("94", "Val-de-Marne"),
        ("95", "Val-d'Oise"),
    )

    department = models.CharField(
        max_length=8,
        choices=DEPARTMENT,
        null=True,
        blank=True,
        verbose_name=_("Département"),
        unique=True,
    )

    groups = models.ManyToManyField(
        to="accounts.Group",
        verbose_name=_("Structures sur ce département"),
        blank=False,
        related_name="actimmo_map",
    )


class ActimmoContact(MixeurBaseModel):
    class Meta:
        verbose_name = _("Contacts des structures lauréates")
        verbose_name_plural = _("Contacts des structures lauréates")

    group = models.ForeignKey(
        "accounts.Group",
        verbose_name=_("Structure"),
        blank=False,
        related_name="actimmo_contact",
        on_delete=models.CASCADE,
    )

    group_profile_pic_overide = models.ImageField(
        upload_to=group_directory_path, blank=True, null=True
    )
    group_name_overide = models.CharField(
        _("overide group name"), max_length=300, blank=True, null=True
    )
    group_full_name_overide = models.CharField(
        _("overide group full name"), max_length=300, blank=True, null=True
    )
    group_website_overide = models.URLField(
        _("overide web site url"), blank=True, null=True
    )
    email = models.EmailField()
    first_name = models.CharField(_("first name"), max_length=300)
    last_name = models.CharField(_("last name"), max_length=300)
    title = models.CharField(
        max_length=100, verbose_name=_("Fonction"), blank=True, null=True
    )
    phone = PhoneNumberField(
        _("Numéro de téléphone"), max_length=100, blank=True, null=True
    )
    group_presentation = models.TextField(
        verbose_name=_("Présentation de la structure"), blank=True, null=True
    )

    @property
    def group_name(self):
        return self.group_name_overide if self.group_name_overide else self.group.name

    @property
    def group_full_name(self):
        return (
            self.group_full_name_overide
            if self.group_full_name_overide
            else self.group.full_name
        )

    @property
    def group_profile_pic(self):
        return (
            self.group_profile_pic_overide
            if self.group_profile_pic_overide
            else self.group.profile_pic
        )

    @property
    def group_website(self):
        return (
            self.group_website_overide
            if self.group_website_overide
            else self.group.website
        )

    @property
    def presentation(self):
        return (
            self.group_presentation
            if self.group_presentation
            else self.group.presentation
        )

# -*- coding: utf-8 -*-
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.shortcuts import reverse
from django.utils.translation import ugettext_lazy as _

from phonenumber_field.modelfields import PhoneNumberField

from accounts.models import User

from core.models import MixeurBaseModel

from .activity import Activity
from .job import Job
from .key_word import KeyWord
from .segment import Segment
from .sub_mission import SubMission


def logo_path(instance, filename):
    return f"professionals/{instance.id}/{filename}"


def logo_original_path(instance, filename):
    return f"professionals/original/{instance.id}/{filename}"


class Professional(MixeurBaseModel):
    class Meta:
        ordering = ["name"]

    name = models.CharField(verbose_name=_("Raison sociale"), max_length=256)
    adress = models.CharField(verbose_name=_("Adresse"), max_length=256)
    town = models.CharField(verbose_name=_("Ville"), max_length=256)
    postcode = models.CharField(
        verbose_name=_("Code postale"),
        max_length=6,
    )

    phone_number = PhoneNumberField(
        verbose_name=_("Téléphone"),
        null=True,
    )

    email = models.EmailField(verbose_name=_("Email"), blank=True)
    url = models.URLField(verbose_name=_("Site web"), blank=True)
    logo = models.ImageField(upload_to=logo_path, blank=True, default=None)
    original_logo = models.ImageField(
        upload_to=logo_original_path, blank=True, default=None
    )
    job = models.ForeignKey(
        Job,
        verbose_name="Sélectionner votre métier",
        blank=True,
        null=True,
        on_delete=models.PROTECT,
    )
    segments = models.ManyToManyField(
        Segment,
        verbose_name="Sélectionner votre segment d'activité",
    )
    activity_first = models.ForeignKey(
        Activity,
        on_delete=models.PROTECT,
        verbose_name="Sélectionner votre domaine d' activité principale",
        related_name="first_choice",
        blank=False,
    )
    activity_second = models.ForeignKey(
        Activity,
        on_delete=models.PROTECT,
        verbose_name="Sélectionner un autre domaine d'activité",
        related_name="second_choice",
        blank=True,
        null=True,
    )
    activity_third = models.ForeignKey(
        Activity,
        on_delete=models.PROTECT,
        verbose_name="Sélectionner un autre domaine d'activité",
        related_name="third_choice",
        blank=True,
        null=True,
    )
    activity_fourth = models.ForeignKey(
        Activity,
        on_delete=models.PROTECT,
        verbose_name="Sélectionner un autre domaine d'activité",
        related_name="fourth_choice",
        blank=True,
        null=True,
    )
    description = models.TextField(
        verbose_name=_("Description longue de votre activité"),
        max_length=1024,
    )
    comment = models.TextField(
        verbose_name=_("Commentaire sur le professionnel"),
        max_length=2000,
        blank=True,
    )
    geom = JSONField(
        verbose_name=_("Localisation du professionel ou de l'entreprise"),
        null=True,
        blank=True,
    )
    primary_key_words = models.ManyToManyField(
        KeyWord,
        verbose_name=_("Sélectionner vos Mots Clés"),
        related_name="primary_key_words",
    )
    secondary_key_words = models.ManyToManyField(
        KeyWord,
        verbose_name=_("Sélectionner vos Mots Clés secondaire"),
        related_name="secondary_key_words",
    )
    personnal_key_words = models.CharField(
        verbose_name=_("Ajouter vos mots-clés"),
        max_length=256,
        blank=True,
    )
    sub_missions = models.ManyToManyField(
        SubMission,
        verbose_name=("Missions proposés"),
        help_text=_(
            "Sélectionnez les missions que vous proposez pour lesquelles vous avez fourni\
                 des références auprès de l'espace info énergie"
        ),
    )

    user = models.ForeignKey(
        User,
        verbose_name=_("Utilisateur"),
        related_name="professional",
        on_delete=models.CASCADE,
    )

    is_in_progress = models.BooleanField(_("En cours de rédaction ?"), default=True)
    pro_is_valid = models.BooleanField(_("Est valide ?"), default=False)

    def __str__(self):
        return self.name

    @property
    def logo_url(self):
        return self.logo

    @property
    def original_logo_url(self):
        return self.original_logo

    @property
    def phone_number_national(self):
        if self.phone_number:
            return self.phone_number
        return ""

    def get_absolute_url(self):
        return reverse("professionals:professional_detail", kwargs={"pk": self.pk})

    def get_form_url(self):
        return reverse("professionals:professional_update_vue", kwargs={"pk": self.pk})

    def get_personnal_key_words_splited(self):
        if self.personnal_key_words:
            key_words = "".join(self.personnal_key_words)
            return key_words.split(",")
        return []

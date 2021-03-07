# -*- coding: utf-8 -*-
from decimal import Decimal
from django.db import models
from core.models import MixeurBaseModel

from django.utils.translation import ugettext_lazy as _

from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError

from .combustible_params import CombustibleParams


# leaves function to not break migrations
def validation_absolute_positive(value):
    if value < 1:
        raise ValidationError(f"Value must be > 1 (was {value}")


class Copro(MixeurBaseModel):
    class Meta:
        verbose_name = _("Informations copropriété")
        verbose_name_plural = _("Informations copropriétés")

    BUILD_YEARS = (
        (1, _("Avant 1948")),
        (2, _("Entre 1948 et 1977")),
        (3, _("Entre 1977 et 2005")),
        (4, _("Après 2005")),
    )

    HEATING_INDIVIDUALISATION_MODES = (
        (1, _("Surface")),
        (2, _("Compteurs de chaleur")),
        (3, _("Répartiteur de chaleur")),
    )

    # COPRO GENERAL INFOS
    name = models.CharField(_("Nom de la copropriété"), max_length=300)
    address = models.CharField(_("Adresse"), max_length=300, blank=True, null=True)

    climatic_zone = models.ForeignKey(
        "autodiag_copro.ClimaticZoneRatio",
        verbose_name=_("Indice de zone climatique"),
        on_delete=models.PROTECT,
    )
    altitude = models.ForeignKey(
        "autodiag_copro.AltitudeRatio",
        verbose_name=_("Altitude"),
        on_delete=models.PROTECT,
    )

    # COPRO DESCRIPTION
    syndic_name = models.CharField(
        _("Nom du syndic"), max_length=300, blank=True, null=True
    )
    number_of_dwellings = models.PositiveSmallIntegerField(
        _("Nombre de logements"), validators=(MinValueValidator(0),), default=1
    )
    number_of_offices_shops = models.PositiveSmallIntegerField(
        _("Nombre de bureaux et commerces"), default=0
    )
    living_area = models.PositiveSmallIntegerField(
        _("Surface habitable totale"), validators=(MinValueValidator(0),)
    )
    number_of_buildings = models.PositiveSmallIntegerField(
        _("Nombre de bâtiments"), validators=(MinValueValidator(0),), default=1
    )
    number_of_floors = models.PositiveSmallIntegerField(_("Nombre d'étages"))
    build_year = models.PositiveSmallIntegerField(
        _("Année de construction"), choices=BUILD_YEARS
    )

    # HEATING INFOS
    heating_is_collective = models.BooleanField(_("Chauffage collectif"), default=False)
    heating_individualisation_mode = models.PositiveSmallIntegerField(
        _("Mode d'individualisation des frais de chauffage"),
        choices=HEATING_INDIVIDUALISATION_MODES,
    )
    heating_individualisation_costs = models.DecimalField(
        _("Frais d'individualisation"),
        validators=(MinValueValidator(Decimal("0")),),
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
    )
    heating_has_maintenance_contract_P2 = models.BooleanField(
        _("Contrat de maintenance P2"), default=False
    )
    heating_maintenance_contract_P2_cost = models.DecimalField(
        _("Montant du contrat de maintenance P2"),
        validators=(MinValueValidator(Decimal("0")),),
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
    )
    heating_has_maintenance_contract_P2_P3 = models.BooleanField(
        _("Contrat de maintenance P2 + P3"), default=False
    )
    heating_maintenance_contract_P2_P3_cost = models.DecimalField(
        _("Montant du contrat de maintenance P2 + P3"),
        validators=(MinValueValidator(Decimal("0")),),
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
    )
    heating_combustible = models.PositiveSmallIntegerField(
        _("Combustible"), choices=CombustibleParams.COMBUSTIBLES
    )

    # HOTWATER INFOS
    hot_water_is_collective = models.BooleanField(
        _("Eau chaude collectif ?"), default=False
    )
    hot_water_has_meters = models.BooleanField(
        _("Avec compteur(s) d'eau chaude ?"), default=False
    )

    # WATER INFOS
    water_is_collective = models.BooleanField(
        _("Eau chaude collectif ?"), default=False
    )
    water_has_meters = models.BooleanField(_("Avec compteur(s) d'eau ?"), default=False)

    # DJU CORRECTION
    with_dju_correction = models.BooleanField(_("Avec correction DJU ?"), default=False)
    ref_dju_correction = models.PositiveSmallIntegerField(
        _("Correction DJU de référence"), null=True, blank=True
    )

    def clean(self):
        if self.heating_is_collective and self.heating_individualisation_mode is None:
            raise ValidationError(
                self.cant_be_blank(Copro.heating_individualisation_mode)
            )

        if self.heating_is_collective and self.heating_individualisation_costs is None:
            raise ValidationError(
                self.cant_be_blank(Copro.heating_individualisation_costs)
            )

        if self.heating_is_collective and self.heating_combustible is None:
            raise ValidationError(self.is_required(Copro.heating_combustible))

        if (
            self.heating_has_maintenance_contract_P2
            and self.heating_maintenance_contract_P2_cost is None
        ):
            raise ValidationError(self.cant_be_blank(Copro.heating_combustible))

        if (
            self.heating_has_maintenance_contract_P2_P3
            and self.heating_maintenance_contract_P2_P3_cost is None
        ):
            raise ValidationError(self.cant_be_blank(Copro.heating_combustible))

        if self.with_dju_correction and self.ref_dju_correction is None:
            raise ValidationError(self.is_required(Copro.ref_dju_correction))

    def cant_be_blank(self, field):
        return _("{field.verbose_name} can't be blank.")

    def is_required(self, field):
        return _("{field.verbose_name} is required.")

    def __str__(self):
        return f"{self.name} - {self.address} - {self.updated_at}"

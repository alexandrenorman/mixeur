# -*- coding: utf-8 -*-
import os

from django.core.files.storage import FileSystemStorage
from django.db import models
from django.utils.translation import ugettext_lazy as _

from core.models import MixeurBaseModel

from helpers.models import representation_helper


fs = FileSystemStorage(location="/media/imported_files")


@representation_helper
class FileImport(MixeurBaseModel):
    class Meta:
        verbose_name = _("Fichier d'import")
        verbose_name_plural = _("Fichiers d'import")

    owning_group = models.ForeignKey(
        "accounts.Group",
        verbose_name=_("Groupe propriétaire"),
        on_delete=models.CASCADE,
        null=False,
        related_name="file_imports",
    )

    description = models.CharField(_("Description"), blank=True, max_length=100)
    imported_file = models.FileField(
        storage=fs, verbose_name=_("Fichier à importer"), max_length=500
    )

    columns_found = models.CharField(
        _("Colonnes trouvées dans l'import"), blank=True, max_length=10000
    )

    columns_not_found = models.CharField(
        _("Colonnes non trouvées dans l'import"), blank=True, max_length=10000
    )

    columns_not_used = models.CharField(
        _("Colonnes exédentaires dans l'import"), blank=True, max_length=10000
    )

    organizations_not_updated = models.ManyToManyField(
        "fac.Organization",
        verbose_name=_("Organisations non mises à jour"),
        blank=True,
        related_name="fileimport_organisations_not_updated",
    )

    contacts_not_updated = models.ManyToManyField(
        "fac.Contact",
        verbose_name=_("Contacts non mises à jour"),
        blank=True,
        related_name="fileimport_contacts_not_updated",
    )

    def delete(self):
        # Delete physical file
        try:
            os.remove(self.imported_file.path)
        except Exception:
            pass

        super(FileImport, self).delete()

    def __str__(self):
        return f"{self.created_at} - {self.description}"

    @property
    def nb_of_contacts(self):
        return self.contact_set.count()

    @property
    def nb_of_organizations(self):
        return self.organization_set.count()

import os
import uuid
from re import search


from django.contrib.staticfiles.templatetags.staticfiles import static
from django.db import models
from django.utils.translation import ugettext_lazy as _

from core.models import MixeurBaseModel

from helpers.fields import SVGField
from helpers.helpers import unique_filename_in_path


def directory_path(instance, filename):
    uid = f"{uuid.uuid4()}"
    dir_path = f"fac/files/icones/{uid[0]}/{uid[:2]}/{uid}"
    valid_file = unique_filename_in_path(dir_path, filename)
    full_path = os.path.join(dir_path, valid_file)
    return full_path


def help_text_icon_marker():
    svg_template_url = static("fac/svg/template.svg")
    help_text = _(
        "Ne prend en charge que les fichiers au format SVG. "
        "Pour une visualisation optimale de votre icône, il faut utiliser "
        f"<a href='{svg_template_url}' download='template.svg'>ce template</a>.\n"
        "Il faut également créer l'icône avec des lignes et non des formes pleines."
    )
    return help_text


class FolderModelQueryset(models.QuerySet):
    def accessible_by(self, user):
        if user.is_administrator:
            return self

        return self.filter(project__groups=user.group)


class FolderModelManager(models.Manager.from_queryset(FolderModelQueryset)):
    def get_queryset(self):
        return super().get_queryset()


class FolderModel(MixeurBaseModel):
    class Meta:
        verbose_name = _("Modèle de dossier")
        verbose_name_plural = _("Modèles de dossier")
        ordering = ["pk"]

    name = models.CharField(verbose_name=_("Nom du modèle de dossier"), max_length=255)
    project = models.ForeignKey(
        "fac.Project",
        verbose_name=_("Projet"),
        on_delete=models.CASCADE,
        related_name="folder_models",
    )
    icon = models.CharField(
        verbose_name=_("Icône de dossier"), default="file-alt", max_length=255
    )
    icon_marker = SVGField(
        _("Icône"),
        upload_to=directory_path,
        null=True,
        blank=True,
        help_text=help_text_icon_marker(),
    )

    link_to_contact = models.BooleanField(
        verbose_name=_("Associer à un contact ?"), default=True
    )
    link_to_organization = models.BooleanField(
        verbose_name=_("Associer à une structure ?"), default=True
    )

    objects = FolderModelManager()

    @property
    def icon_marker_content(self):
        try:
            self.icon_marker.seek(0)
            content = self.icon_marker.read()
            extract = search(b'svg">(.*)</svg', content.replace(b"\n", b"")).group(1)
            return str(extract.decode())
        except Exception:
            return ""

    def __str__(self):
        return f"{self.project.name} - {self.name}"

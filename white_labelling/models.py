# -*- coding: utf-8 -*-
import os

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext_lazy as _

from helpers.models import representation_helper

from white_labelling.helpers import generate_traefik_configuration, wl_cdn


class WhiteLabellingQueryset(models.QuerySet):
    pass


class WhiteLabellingManager(models.Manager.from_queryset(WhiteLabellingQueryset)):
    def default(self):
        return self.filter(is_default=True).first()


@representation_helper
class WhiteLabelling(models.Model):
    class Meta:
        verbose_name = _("Personnalisation marque blanche")
        ordering = ["pk"]

    objects = WhiteLabellingManager()

    domain = models.CharField(
        verbose_name=_("Nom de domaine concerné par la marque blanche"),
        max_length=200,
        blank=True,
        null=True,
        unique=True,
    )

    enable_django_admin = models.BooleanField(
        _("Accès admin django"),
        default=False,
        help_text=_(
            "Cela nécessite impérativement la création d'un enregistrement DNS "
            + "api-DOMAIN. Sinon cela pose problème avec let's encrypt."
        ),
    )

    smtp_account = models.ForeignKey(
        "messaging.SmtpAccount",
        verbose_name=_("Compte SMTP spécifique"),
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="white_labelling",
        limit_choices_to={"is_active": True},
    )
    sms_account = models.ForeignKey(
        "messaging.SmsAccount",
        verbose_name=_("Compte SMS spécifique"),
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="white_labelling",
        limit_choices_to={"is_active": True},
    )
    site_title = models.CharField(
        verbose_name=_("Titre du site"), max_length=200, blank=True, default=""
    )
    site_baseline = models.CharField(
        verbose_name=_("Baseline du site"),
        default="Mes services Espace Info Energie",
        max_length=200,
        blank=True,
        help_text="HTML autorisé",
    )
    is_active = models.BooleanField(_("Domaine actif"), default=True)
    is_default = models.BooleanField(_("Domaine par défaut"), default=False)
    is_neutral_for_newsletters = models.BooleanField(
        _("Domaine neutre pour les newsletters"), default=False
    )
    has_breadcrumb = models.BooleanField(_("Montrer le fil d'ariane ?"), default=True)
    has_menu = models.BooleanField(_("Montrer le menu ?"), default=True)
    has_main_header = models.BooleanField(
        _("Montrer le bandeau générique ?"), default=True
    )
    home_route = models.CharField(
        verbose_name=_("Route de la homepage - utilisateur non connectés"),
        max_length=100,
        blank=True,
        default="AccountLogin",
        help_text="La route peut prendre des paramètres sous la forme RouteName:param1=x:param2=y",
    )
    home_route_for_client = models.CharField(
        verbose_name=_("Route de la homepage - clients"),
        max_length=100,
        blank=True,
        default="DashboardClient",
    )
    home_route_for_professional = models.CharField(
        verbose_name=_("Route de la homepage - professionnels"),
        max_length=100,
        blank=True,
        default="Home",
    )
    home_route_for_advisor = models.CharField(
        verbose_name=_("Route de la homepage - conseillers"),
        max_length=100,
        blank=True,
        default="FacContactsList",
        help_text="La route peut prendre des paramètres sous la forme RouteName:param1=x:param2=y",
    )
    home_route_for_manager = models.CharField(
        verbose_name=_("Route de la homepage - managers"),
        max_length=100,
        blank=True,
        default="GroupList",
        help_text="La route peut prendre des paramètres sous la forme RouteName:param1=x:param2=y",
    )
    home_route_for_administrator = models.CharField(
        verbose_name=_("Route de la homepage - administrateurs"),
        max_length=100,
        blank=True,
        default="GroupList",
        help_text="La route peut prendre des paramètres sous la forme RouteName:param1=x:param2=y",
    )
    usermanagement_is_active = models.BooleanField(
        _("Activer la gestion des utilisateurs"), default=True
    )

    clientselfcreation_is_active = models.BooleanField(
        _("Activer l'auto créations des utilisateurs clients"), default=False
    )

    actimmo_map_is_active = models.BooleanField(
        _("Activer la cartographie actimmo"), default=False
    )
    actimmo_map_remove_margins = models.BooleanField(
        _("Supprimer les marges sur la cartographie (pour iframe)"), default=False
    )
    actimmo_partners_on_map_is_active = models.BooleanField(
        _("Montrer les partenaires sur la cartographie actimmo"), default=False
    )
    actimmo_map_name = models.CharField(
        verbose_name=_("Nom de l'application ActimmoMap"),
        max_length=100,
        default="ActimmoMap",
    )
    actimmo_map_baseline = models.CharField(
        verbose_name=_("Cartographie de l'avancement actimmo"),
        max_length=100,
        default="Cartographie de l'avancement actimmo",
    )

    autodiag_is_active = models.BooleanField(_("Activer Autodiagcopro"), default=False)
    autodiag_name = models.CharField(
        verbose_name=_("Nom de l'application AutodiagCopro"),
        max_length=100,
        default="AutodiagCopro",
    )
    autodiag_baseline = models.CharField(
        verbose_name=_("Baseline de l'application AutodiagCopro"),
        max_length=100,
        default="Comparer les performances énergétique de ma copropriété",
    )

    dialogwatt_is_active = models.BooleanField(_("Activer Dialogwatt"), default=False)
    dialogwatt_name = models.CharField(
        verbose_name=_("Nom de l'application DialogWatt"),
        max_length=100,
        default="DialogWatt",
    )
    dialogwatt_baseline = models.CharField(
        verbose_name=_("Baseline de l'application DialogWatt"),
        max_length=100,
        default="Prendre rendez-vous avec mon conseiller info-énergie",
    )

    visit_report_is_active = models.BooleanField(
        _("Activer le Compte-Rendu de visites"), default=True
    )
    preco_immo_is_active = models.BooleanField(
        _("Activer les Préco'Immo"), default=True
    )
    visit_report_show_wip = models.BooleanField(
        _("Afficher le message de travaux"), default=True
    )
    visit_report_name = models.CharField(
        verbose_name=_("Nom de l'application Rapport de visite"),
        max_length=100,
        default="Compte rendu de RDV",
    )
    visit_report_baseline = models.CharField(
        verbose_name=_("Baseline de l'application Rapport de visite"),
        max_length=100,
        default="Édition de rapport entretien logement",
    )
    preco_immo_name = models.CharField(
        verbose_name=_("Nom de l'application Préco'Immo"),
        max_length=100,
        default="Préco'IMMO",
    )
    preco_immo_baseline = models.CharField(
        verbose_name=_("Baseline de l'application Préco'immo"),
        max_length=100,
        default="Édition de rapport entretien logement",
    )

    thermix_is_active = models.BooleanField(_("Activer Thermix"), default=False)
    thermix_name = models.CharField(
        verbose_name=_("Nom de l'application Thermix"),
        max_length=100,
        default="Thermix",
    )
    thermix_baseline = models.CharField(
        verbose_name=_("Baseline de l'application Thermix"),
        max_length=100,
        default="Comparer les systèmes de production de chauffage",
    )

    therminix_is_active = models.BooleanField(_("Activer Therminix"), default=False)
    therminix_name = models.CharField(
        verbose_name=_("Nom de l'application Therminix"),
        max_length=100,
        default="Therminix",
    )
    therminix_baseline = models.CharField(
        verbose_name=_("Baseline de l'application Therminix"),
        max_length=100,
        default="Proposition de solutions de chauffages",
    )

    old_thermix_is_active = models.BooleanField(
        _("Activer l'ancien Thermix en iframe"), default=True
    )
    old_thermix_name = models.CharField(
        verbose_name=_("Nom de l'application Thermix (iframe)"),
        max_length=100,
        default="Thermix",
    )
    old_thermix_baseline = models.CharField(
        verbose_name=_("Baseline de l'application Thermix (iframe)"),
        max_length=100,
        default="Comparer les systèmes de production de chauffage",
    )

    simulaides_is_active = models.BooleanField(_("Activer Simulaides"), default=False)
    simulaides_name = models.CharField(
        verbose_name=_("Nom de l'application Simulaides"),
        max_length=100,
        default="Simulaides",
    )
    simulaides_baseline = models.CharField(
        verbose_name=_("Baseline de l'application Simulaides"),
        max_length=100,
        default="Simuler les aides mobilisables pour le financement de mes travaux",
    )

    # Ecorenover iframe
    ecorenover_iframe_is_active = models.BooleanField(
        _("Activer Écorénover (iFrame)"), default=True
    )
    ecorenover_iframe_name = models.CharField(
        verbose_name=_("Nom de l'application Écorénover (iFrame)"),
        max_length=100,
        default="Écorénover",
    )
    ecorenover_iframe_baseline = models.CharField(
        verbose_name=_("Baseline de l'application Écorénover (iFrame)"),
        max_length=100,
        default="Construction d'un plan de financement pour mes rénovations",
    )

    # Ecorenover normal
    ecorenover_is_active = models.BooleanField(_("Activer Écorénover"), default=False)
    ecorenover_save_to_fac = models.BooleanField(
        _("Activer la sauvegarde de simulations Écorénover dans FAC"), default=False
    )
    ecorenover_name = models.CharField(
        verbose_name=_("Nom de l'application Écorénover"),
        max_length=100,
        default="Écorénover",
    )
    ecorenover_baseline = models.CharField(
        verbose_name=_("Baseline de l'application Écorénover"),
        max_length=100,
        default="Construction d'un plan de financement pour mes rénovations",
    )

    fac_is_active = models.BooleanField(_("Activer Fabrique à contacts"), default=True)
    fac_name = models.CharField(
        verbose_name=("Nom de l'application Fabrique à contacts"),
        max_length=100,
        default="Fabrique à contacts",
    )
    fac_baseline = models.CharField(
        verbose_name=_("Baseline de l'application Fabrique à Contacts"),
        max_length=100,
        default="Outil de gestion de contacts",
    )
    fac_hide_lists = models.BooleanField(_("Cacher les listes"), default=True)
    fac_statistics_is_active = models.BooleanField(
        _("Activer l'onglet 'Statistiques' de FAC"), default=False
    )

    newsletters_is_active = models.BooleanField(
        _("Activer les newsletters"), default=False
    )
    newsletters_name = models.CharField(
        verbose_name=("Nom de l'application newsletters"),
        max_length=100,
        default="Newsletters",
    )
    newsletters_baseline = models.CharField(
        verbose_name=_("Baseline de l'application newsletters"),
        max_length=100,
        default="Outil de création de newsletters",
    )
    newsletters_public_name = models.CharField(
        verbose_name=("Nom de l'application publique newsletters"),
        max_length=100,
        default="Newsletters",
    )
    newsletters_public_baseline = models.CharField(
        verbose_name=_("Baseline de l'application publique newsletters"),
        max_length=100,
        default="Newsletters",
    )

    experiences_is_active = models.BooleanField(
        _("Activer les références"), default=False
    )
    experiences_name = models.CharField(
        verbose_name=("Nom de l'application références"),
        max_length=100,
        default="Experiences",
    )
    experiences_baseline = models.CharField(
        verbose_name=_("Baseline de l'application références"),
        max_length=100,
        default="Outil de recueil de références",
    )

    listepro_is_active = models.BooleanField(_("Activer la listepro"), default=False)
    listepro_name = models.CharField(
        verbose_name=("Nom de l'application listepro"),
        max_length=100,
        default="Liste Pro",
    )
    listepro_baseline = models.CharField(
        verbose_name=_("Baseline de l'application listepro"),
        max_length=100,
        default="Rechercher des professionnels du bâtiment",
    )

    # Matomo
    matomo_url = models.CharField(
        verbose_name=_("Url matomo"),
        max_length=200,
        default="https://statspiwik.hespul.org",
    )
    matomo_site_id = models.IntegerField(verbose_name=_("SiteId matomo"), default=34)
    matomo_tracker_file_name = models.CharField(
        verbose_name=_("Tracker filename matomo"), max_length=200, default="piwik"
    )

    def __str__(self):
        return f"{self.domain} - {self.site_title}"

    @property
    def name(self):
        return self.site_title

    @classmethod
    def default(cls):
        return cls.objects.default()

    def clean(self):
        if (
            self.is_default
            and WhiteLabelling.objects.exclude(pk=self.pk)
            .filter(is_default=True)
            .exists()
        ):
            raise ValidationError(
                _(
                    "Il n'est possible d'avoir qu'une seule marque blanche par défaut par serveur."
                )
            )
        if (
            self.is_neutral_for_newsletters
            and WhiteLabelling.objects.exclude(pk=self.pk)
            .filter(is_neutral_for_newsletters=True)
            .exists()
        ):
            raise ValidationError(
                _(
                    "Il n'est possible d'avoir qu'une seule marque blanche neutre pour les newsletters par serveur."
                )
            )
        if self.old_thermix_is_active and self.thermix_is_active:
            raise ValidationError(
                _(
                    "Il n'est pas possible d'activer simultanément l'ancienne et la nouvelle version de Thermix"
                )
            )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # on save, regenerate traefik configuration
        if not settings.SKIP_TRAEFIK_AUTOCONFIG_ON_WL_SAVE:
            generate_traefik_configuration()

        self.create_cdn_files()
        return

    def create_cdn_files(self):
        if not os.path.exists(self.cdn_directory_path):
            os.mkdir(self.cdn_directory_path)
            for filename in ["style.css", "header.html", "footer.html", "favicon.png"]:
                f = open(os.path.join(self.cdn_directory_path, filename), "w")
                f.write("")
                f.close()

    @property
    def cdn_directory_path(self):
        return f"/app/wl-cdn/{self.domain}"

    @property
    def cdn_default_directory_path(self):
        return "/app/wl-cdn-default/"

    @property
    def cdn_data(self):
        return wl_cdn.read_data(self)

    def get_cdn_data(self, path: str = None):
        return wl_cdn.get_data(self, path)

    def get_cdn_text(self, path: str, params: dict = None, fallback: str = None):
        params = params if params is not None else {}
        return wl_cdn.get_text(self, path, params, fallback)

    @property
    def domain_as_string(self):
        return self.domain.replace(".", "_")

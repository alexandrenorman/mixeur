# -*- coding: utf-8 -*-
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from accounts.models import User

from .models import WhiteLabelling


def disable_white_labelling(modeladmin, request, queryset):
    for obj in queryset:
        obj.is_active = False
        obj.save()


disable_white_labelling.short_description = "Désactiver la marque blanche"


def disable_django_admin(modeladmin, request, queryset):
    for obj in queryset:
        obj.enable_django_admin = False
        obj.save()


disable_django_admin.short_description = "Désactiver l'entrée admin django"


def enable_django_admin(modeladmin, request, queryset):
    for obj in queryset:
        obj.enable_django_admin = True
        obj.save()


enable_django_admin.short_description = "Activer l'entrée admin django"


def enable_white_labelling(modeladmin, request, queryset):
    for obj in queryset:
        obj.is_active = True
        obj.save()


enable_white_labelling.short_description = "Activer la marque blanche"


def duplicate_white_labelling(modeladmin, request, queryset):
    for obj in queryset:
        obj.pk = None
        obj.domain = obj.domain + "-copy"
        obj.is_active = False
        obj.is_default = False
        obj.save()


duplicate_white_labelling.short_description = "Dupliquer la marque blanche"


@admin.register(WhiteLabelling)
class WhiteLabellingAdmin(admin.ModelAdmin):
    list_display = [
        "domain",
        "groups",
        "site_title",
        "is_active",
        "enable_django_admin",
        "is_default",
        "is_neutral_for_newsletters",
        "has_breadcrumb",
        "has_menu",
        "nb_of_users",
        "usermanagement_is_active",
        "clientselfcreation_is_active",
        "actimmo_map_is_active",
        "actimmo_partners_on_map_is_active",
        "autodiag_is_active",
        "dialogwatt_is_active",
        "ecorenover_iframe_is_active",
        "ecorenover_is_active",
        "experiences_is_active",
        "fac_is_active",
        "fac_statistics_is_active",
        "listepro_is_active",
        "newsletters_is_active",
        "old_thermix_is_active",
        "preco_immo_is_active",
        "visit_report_is_active",
        "therminix_is_active",
        "thermix_is_active",
        "simulaides_is_active",
    ]
    list_filter = ("is_active",)
    search_fields = ("domain", "site_title")
    exclude = []

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "domain",
                    "is_active",
                    "enable_django_admin",
                    "is_default",
                    "is_neutral_for_newsletters",
                    "smtp_account",
                    "sms_account",
                    "site_title",
                    "site_baseline",
                    "has_breadcrumb",
                    "has_menu",
                    "has_main_header",
                )
            },
        ),
        (
            "Routes par défaut",
            {
                "fields": (
                    "home_route",
                    "home_route_for_client",
                    "home_route_for_professional",
                    "home_route_for_advisor",
                    "home_route_for_manager",
                    "home_route_for_administrator",
                )
            },
        ),
        (
            "Gestion des utilisateurs",
            {"fields": ("usermanagement_is_active", "clientselfcreation_is_active")},
        ),
        (
            "Cartographie actimmo",
            {
                "fields": (
                    "actimmo_map_is_active",
                    "actimmo_map_remove_margins",
                    "actimmo_partners_on_map_is_active",
                    "actimmo_map_name",
                    "actimmo_map_baseline",
                )
            },
        ),
        (
            "Autodiagcopro",
            {"fields": ("autodiag_is_active", "autodiag_name", "autodiag_baseline")},
        ),
        (
            "Dialogwatt",
            {
                "fields": (
                    "dialogwatt_is_active",
                    "dialogwatt_name",
                    "dialogwatt_baseline",
                )
            },
        ),
        (
            "Compte rendu de visites",
            {
                "fields": (
                    "visit_report_is_active",
                    "visit_report_name",
                    "visit_report_baseline",
                    "preco_immo_is_active",
                    "preco_immo_name",
                    "preco_immo_baseline",
                    "visit_report_show_wip",
                )
            },
        ),
        (
            "Thermix",
            {
                "fields": (
                    "thermix_is_active",
                    "thermix_name",
                    "thermix_baseline",
                    "old_thermix_is_active",
                    "old_thermix_name",
                    "old_thermix_baseline",
                    "therminix_is_active",
                    "therminix_name",
                    "therminix_baseline",
                )
            },
        ),
        (
            "Simulaides",
            {
                "fields": (
                    "simulaides_is_active",
                    "simulaides_name",
                    "simulaides_baseline",
                )
            },
        ),
        (
            "Écorénover IFRAME",
            {
                "fields": (
                    "ecorenover_iframe_is_active",
                    "ecorenover_iframe_name",
                    "ecorenover_iframe_baseline",
                )
            },
        ),
        (
            "Écorénover",
            {
                "fields": (
                    "ecorenover_is_active",
                    "ecorenover_save_to_fac",
                    "ecorenover_name",
                    "ecorenover_baseline",
                )
            },
        ),
        (
            "FAC / FAP",
            {
                "fields": (
                    "fac_is_active",
                    "fac_name",
                    "fac_baseline",
                    "fac_hide_lists",
                    "fac_statistics_is_active",
                )
            },
        ),
        (
            "Newsletters",
            {
                "fields": (
                    "newsletters_is_active",
                    "newsletters_name",
                    "newsletters_baseline",
                    "newsletters_public_name",
                    "newsletters_public_baseline",
                )
            },
        ),
        (
            "Experiences",
            {
                "fields": (
                    "experiences_is_active",
                    "experiences_name",
                    "experiences_baseline",
                )
            },
        ),
        (
            "Liste Pro",
            {
                "fields": (
                    "listepro_is_active",
                    "listepro_name",
                    "listepro_baseline",
                )
            },
        ),
        (
            "Matomo",
            {"fields": ("matomo_url", "matomo_site_id", "matomo_tracker_file_name")},
        ),
    )

    def nb_of_users(self, obj):
        return User.objects.filter(white_labelling=obj).count()

    nb_of_users.short_description = _("Nombre d'utilisateurs")

    def groups(self, obj):
        return ", ".join([str(x) for x in obj.group.all()])

    groups.short_description = _("Groupes")

    actions = [
        disable_white_labelling,
        duplicate_white_labelling,
        enable_white_labelling,
        disable_django_admin,
        enable_django_admin,
    ]

# -*- coding: utf-8 -*-
from django import forms
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from white_labelling.models import WhiteLabelling

from .models import Group, RgpdConsent, User


# Group's stuff ###########$


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "preferred_white_labelling",
        "is_admin",
        "admin_group",
        "users",
        "ademe_id",
    ]
    search_fields = ("name", "white_labelling__domain")
    exclude = ["territories"]
    prepopulated_fields = {"slug": ("name",)}

    def users(self, obj):
        return ", ".join([str(x) for x in obj.users])

    users.short_description = _("Membres")


# RgpdConsent's stuff ###########$


@admin.register(RgpdConsent)
class RgpdConsentAdmin(admin.ModelAdmin):
    list_display = ["creation_date"]
    exclude = []


# User's stuff ###########$


def send_initialize_account_url(modeladmin, request, queryset):
    for obj in queryset:
        obj.send_initialize_account_url()


send_initialize_account_url.short_description = _(
    "Envoyer l'email de bienvenue avec le lien pour initialiser son compte."
)


def send_reset_password_url(modeladmin, request, queryset):
    for obj in queryset:
        obj.send_reset_password_url()


send_reset_password_url.short_description = _("Envoyer l'email de reset de password.")


class UserRgpdConsentInline(admin.StackedInline):
    model = RgpdConsent
    extra = 0
    readonly_fields = ("creation_date",)


class UserAdminForm(forms.ModelForm):
    class Meta:
        model = User
        exclude = []

    group = forms.ModelChoiceField(
        queryset=Group.objects.order_by("name"), required=False
    )
    white_labelling = forms.ModelChoiceField(
        queryset=WhiteLabelling.objects.order_by("domain"), required=False
    )


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    base_model = User
    form = UserAdminForm

    list_display = [
        "email",
        "civility",
        "first_name",
        "last_name",
        "is_staff",
        "is_active",
        "date_joined",
        "profile_type",
        "group",
        "white_labelling",
    ]
    list_filter = ("is_staff", "is_active", "user_type", "group")
    inlines = [UserRgpdConsentInline]
    search_fields = ("first_name", "last_name", "email")
    exclude = ["password"]
    actions = [send_initialize_account_url, send_reset_password_url]

    def profile_type(self, obj):
        return obj.get_user_type_display()

    profile_type.short_description = _("Profile")

    def domain(self, obj):
        if obj.white_labelling:
            return obj.white_labelling.domain

        return "-"

    domain.short_description = _("Domaine")

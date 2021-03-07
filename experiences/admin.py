# -*- coding: utf-8 -*-
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django import forms

from accounts.models import Group


from .models import (
    AssignmentTag,
    Experience,
    ExperienceSponsor,
    ExperienceTag,
    Explanation,
    JobTag,
    PartnerTag,
    PublicTag,
    SponsorTag,
    YearTag,
)


class ExperienceForm(forms.ModelForm):
    owning_group = forms.ModelChoiceField(queryset=Group.objects.all().order_by("name"))

    class Meta:
        model = Experience
        exclude = []


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    base_model = Experience
    list_display = ["pk", "title", "referent", "ctags"]
    search_fields = ("title", "tags__name")
    exclude = []
    form = ExperienceForm

    owning_group = forms.ModelChoiceField(queryset=Group.objects.all().order_by("name"))

    def ctags(self, obj):
        return ", ".join([str(x) for x in obj.tags.all()])

    ctags.short_description = _("Tags")


class ExperienceSponsorForm(forms.ModelForm):
    owning_group = forms.ModelChoiceField(queryset=Group.objects.all().order_by("name"))

    class Meta:
        model = ExperienceSponsor
        exclude = []


@admin.register(ExperienceSponsor)
class ExperienceSponsorAdmin(admin.ModelAdmin):
    base_model = ExperienceSponsor
    list_display = ["pk", "title", "sponsor"]
    search_fields = ("title", "tags__name")
    exclude = []
    form = ExperienceSponsorForm

    owning_group = forms.ModelChoiceField(queryset=Group.objects.all().order_by("name"))

    def ctags(self, obj):
        return ", ".join([str(x) for x in obj.tags.all()])

    ctags.short_description = _("Tags")


class AssignmentTagForm(forms.ModelForm):
    owning_group = forms.ModelChoiceField(queryset=Group.objects.all().order_by("name"))

    class Meta:
        model = AssignmentTag
        exclude = []


@admin.register(AssignmentTag)
class AssignmentTagAdmin(admin.ModelAdmin):
    list_display = ["pk", "name"]
    search_fields = ("name",)
    exclude = []
    base_model = AssignmentTag
    form = AssignmentTagForm

    owning_group = forms.ModelChoiceField(queryset=Group.objects.all().order_by("name"))


class ExperienceTagForm(forms.ModelForm):
    owning_group = forms.ModelChoiceField(queryset=Group.objects.all().order_by("name"))

    class Meta:
        model = ExperienceTag
        exclude = []


@admin.register(ExperienceTag)
class ExperienceTagAdmin(admin.ModelAdmin):
    list_display = ["pk", "name"]
    search_fields = ("name",)
    exclude = []
    base_model = ExperienceTag
    form = ExperienceTagForm

    owning_group = forms.ModelChoiceField(queryset=Group.objects.all().order_by("name"))


class JobTagForm(forms.ModelForm):
    owning_group = forms.ModelChoiceField(queryset=Group.objects.all().order_by("name"))

    class Meta:
        model = JobTag
        exclude = []


@admin.register(JobTag)
class JobTagAdmin(admin.ModelAdmin):
    list_display = ["pk", "name"]
    search_fields = ("name",)
    exclude = []
    base_model = JobTag
    form = JobTagForm

    owning_group = forms.ModelChoiceField(queryset=Group.objects.all().order_by("name"))


class PartnerTagForm(forms.ModelForm):
    owning_group = forms.ModelChoiceField(queryset=Group.objects.all().order_by("name"))

    class Meta:
        model = PartnerTag
        exclude = []


@admin.register(PartnerTag)
class PartnerTagAdmin(admin.ModelAdmin):
    list_display = ["pk", "name"]
    search_fields = ("name",)
    exclude = []
    base_model = PartnerTag
    form = PartnerTagForm


class PublicTagForm(forms.ModelForm):
    owning_group = forms.ModelChoiceField(queryset=Group.objects.all().order_by("name"))

    class Meta:
        model = PublicTag
        exclude = []


@admin.register(PublicTag)
class PublicTagAdmin(admin.ModelAdmin):
    list_display = ["pk", "name"]
    search_fields = ("name",)
    exclude = []
    base_model = PublicTag
    form = PublicTagForm

    owning_group = forms.ModelChoiceField(queryset=Group.objects.all().order_by("name"))


class SponsorTagForm(forms.ModelForm):
    owning_group = forms.ModelChoiceField(queryset=Group.objects.all().order_by("name"))

    class Meta:
        model = SponsorTag
        exclude = []


@admin.register(SponsorTag)
class SponsorTagAdmin(admin.ModelAdmin):
    list_display = ["pk", "name"]
    search_fields = ("name",)
    exclude = []
    base_model = SponsorTag
    form = SponsorTagForm

    owning_group = forms.ModelChoiceField(queryset=Group.objects.all().order_by("name"))


class YearTagForm(forms.ModelForm):
    owning_group = forms.ModelChoiceField(queryset=Group.objects.all().order_by("name"))

    class Meta:
        model = YearTag
        exclude = []


@admin.register(YearTag)
class YearTagAdmin(admin.ModelAdmin):
    list_display = ["pk", "name"]
    search_fields = ("name",)
    exclude = []
    base_model = YearTag
    form = YearTagForm

    owning_group = forms.ModelChoiceField(queryset=Group.objects.all().order_by("name"))


class ExplanationForm(forms.ModelForm):
    owning_group = forms.ModelChoiceField(queryset=Group.objects.all().order_by("name"))

    class Meta:
        model = YearTag
        exclude = []


@admin.register(Explanation)
class ExplanationAdmin(admin.ModelAdmin):
    base_model = Explanation
    list_display = ["pk", "owning_group"]
    exclude = []
    form = ExplanationForm

    owning_group = forms.ModelChoiceField(queryset=Group.objects.all().order_by("name"))

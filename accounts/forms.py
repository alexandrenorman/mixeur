# -*- coding: utf-8 -*-
from django import forms

from .models import Group, RgpdConsent, User

from django.utils.translation import ugettext_lazy as _
from helpers.forms import JsonFileField


class AccountForm(forms.ModelForm):
    error_css_class = "error"
    required_css_class = "required"

    class Meta:
        model = User
        fields = ("civility", "first_name", "last_name")
        exclude = ("email", "password")


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = (
            "name",
            "full_name",
            "is_active",
            "is_admin",
            "admin_group",
            "presentation",
            "phone",
            "email",
            "profile_pic",
            "website",
            "address",
        )

    profile_pic = JsonFileField(required=False)
    admin_group = forms.ModelChoiceField(
        queryset=Group.objects.filter(is_admin=True), required=False, to_field_name="pk"
    )


class GroupPartialForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ("presentation", "phone", "email", "profile_pic", "website", "address")

    profile_pic = JsonFileField(required=False)


class RgpdConsentForm(forms.ModelForm):
    class Meta:
        model = RgpdConsent
        fields = (
            "user",
            "allow_to_keep_data",
            "allow_to_use_phone_number_to_send_reminder",
            "allow_to_use_email_to_send_reminder",
            "allow_to_share_my_information_with_my_advisor",
            "allow_to_share_my_information_with_partners",
        )


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            "email",
            "first_name",
            "last_name",
            "user_type",
            "phone",
            "color",
            "title",
            "group",
            "is_active",
        )

    user_type = forms.CharField(required=False)
    color = forms.CharField(required=False)
    is_active = forms.BooleanField(required=False)

    def clean_email(self):
        email = self.cleaned_data["email"]
        email = email.lower()
        return email


class ResetPasswordForm(forms.Form):
    email = forms.EmailField()


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField()
    new_password1 = forms.CharField()
    new_password2 = forms.CharField()

    def clean(self):
        """
        Verifies that the values entered into the password fields match

        NOTE: Errors here will appear in ``non_field_errors()`` because it applies to more than one field.
        """
        super().clean()
        if "password1" in self.cleaned_data and "password2" in self.cleaned_data:
            if self.cleaned_data["password1"] != self.cleaned_data["password2"]:
                raise forms.ValidationError(
                    _("The passwords did not match. Please try again.")
                )
        return self.cleaned_data

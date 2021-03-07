# -*- coding: utf-8 -*-
from django import forms
from django.contrib.contenttypes.fields import GenericForeignKey
from django.core.exceptions import ValidationError

from accounts.models import User

from fac.models import Contact


class ClientOrContactGenericForeignKey(GenericForeignKey):
    def __get__(self, instance, cls=None):
        obj = super().__get__(instance, cls)
        return self._proxifying_contact(obj)

    def _proxifying_contact(self, obj):
        """
        Return an User or a proxied Contact which mimic a User
        """
        if obj is None:
            return obj

        if obj._meta.label == "fac.Contact":
            # Init object without DB hit
            # equ to FacContactForDialogwatt.objects.get(pk=obj.pk)
            from dialogwatt.models import FacContactForDialogwatt

            o = FacContactForDialogwatt()
            o.__dict__ = obj.__dict__
            return o

        elif obj._meta.label == "accounts.User":
            return obj

        return obj


class ClientOrContactField(forms.Field):
    # Validate a Client or a Contact such as :
    # * {'value': User.objects.last().pk, 'user': []}
    # * {'value': Contact.objects.last().pk, 'contact': []}

    def __init__(  # NOQA:CFQ002
        self,
        *,
        required=True,
        widget=None,
        label=None,
        initial=None,
        help_text="",
        error_messages=None,
        show_hidden_initial=False,
        validators=(),
        localize=False,
        disabled=False,
        label_suffix=None,
    ):
        super().__init__()
        self.required = required

    def _get_user_instance(self, value):
        pk = None
        if "value" in value:
            pk = value["value"]
        elif "pk" in value:
            pk = value["pk"]

        try:
            instance = User.clients.get(pk=pk)
        except User.DoesNotExist:
            raise ValidationError(f"Invalid value [User.DoesNotExist] ({pk})")

        return instance

    def _get_contact_instance(self, value):
        pk = None
        if "value" in value:
            pk = value["value"]
        elif "pk" in value:
            pk = value["pk"]

        try:
            instance = Contact.objects.get(pk=pk)
        except Contact.DoesNotExist:
            raise ValidationError(f"Invalid value [Contact.DoesNotExist] ({pk})")

        return instance

    def clean(self, value):
        if value is None:
            if not self.required:
                return None
            else:
                return ValidationError("Required value")

        if "user_type" in value.keys() and value["user_type"] == "client":
            return User.clients.get(pk=value["pk"])

        elif "is_contact" in value.keys() and value["is_contact"]:
            return Contact.objects.get(pk=value["pk"])

        elif "client" in value.keys() and value["value"]:
            return self._get_user_instance(value)

        elif "contact" in value.keys() and value["value"]:
            return self._get_contact_instance(value)

        raise ValidationError(f"Unknown value {value}")

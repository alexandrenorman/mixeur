from fac.models import Organization, Contact
from django.core.exceptions import ValidationError
from django import forms


class OrganizationOrContactField(forms.Field):
    # Validate a Organization or a Contact such as :
    #   {'pk': Organization.objects.last().pk, 'type': 'organisation'}
    #   {'pk': Contact.objects.last().pk, 'type': 'contact'}

    def _get_organization_instance(self, value):
        try:
            return Organization.objects.get(pk=value["pk"])
        except Organization.DoesNotExist:
            raise ValidationError("Invalid value [Organization.DoesNotExist]")

    def _get_contact_instance(self, value):
        try:
            return Contact.objects.get(pk=value["pk"])
        except Contact.DoesNotExist:
            raise ValidationError("Invalid value [Contact.DoesNotExist]")

    def clean(self, value):
        if value is None:
            if self.required:
                raise ValidationError("Required value")
            return None

        if value.get("type") == "contact":
            return self._get_contact_instance(value)
        elif value.get("type") == "organization":
            return self._get_organization_instance(value)

        raise ValidationError(f"Unknown value {value}")

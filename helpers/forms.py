# -*- coding: utf-8 -*-
import base64
from io import BytesIO

from django import forms
from django.core.exceptions import ValidationError
from django.utils.dateparse import parse_datetime
from django.utils.encoding import force_str
from django.forms.widgets import DateTimeInput
from django.utils.translation import gettext_lazy as _
from django.core.files.uploadedfile import InMemoryUploadedFile


class FormProxy:
    def __init__(self, form):
        self.form = form

    def __getattribute__(self, name):
        if name != "form" and name in self.form.fields:
            return self.form.cleaned_data[name]
        return super().__getattribute__(name)


class SelectToCharField(forms.CharField):
    def to_python(self, value):
        """
        Return a string (value).
        From a dict { value, label }
        """
        if value not in self.empty_values and value["value"] not in self.empty_values:
            value = str(value["value"])
            if self.strip:
                value = value.strip()
        if value in self.empty_values:
            return self.empty_value
        return value


class OptionListField(forms.Field):
    def __init__(
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
        queryset=None,
    ):
        super().__init__()
        self.queryset = queryset
        self.required = required

    def clean(self, value):
        if value is None:
            if not self.required:
                return None
            else:
                raise ValidationError("Required value")

        if "value" in value:
            try:
                instance = self.queryset.get(pk=value["value"])
            except self.queryset.model.DoesNotExist:
                raise ValidationError("Invalid value", value)
        elif "pk" in value:
            try:
                instance = self.queryset.get(pk=value["pk"])
            except self.queryset.model.DoesNotExist:
                raise ValidationError("Invalid value", value)
        else:
            raise ValidationError("Invalid value", value)

        return instance


class ISODateTimeField(forms.Field):
    """DateTimeField that uses django.utils.dateparse.parse_datetime.

    More precisely, this DateTimeField accepts ISO 8601 datetime strings
    that specify timezone with +00:00 syntax.

    https://en.wikipedia.org/wiki/ISO_8601
    https://code.djangoproject.com/ticket/11385
    https://bugs.python.org/issue15873
    https://bugs.python.org/msg169952
    """

    widget = DateTimeInput
    default_error_messages = {"invalid": _("Enter a valid date/time.")}

    def to_python(self, value):
        if value is None:
            return None

        value = value.strip()
        try:
            return self.strptime(value, format)
        except (ValueError, TypeError):
            raise forms.ValidationError(self.error_messages["invalid"], code="invalid")

    def strptime(self, value, format):
        return parse_datetime(force_str(value))


class JsonFileField(forms.Field):
    """
    A FileField which works with json forms

    await a dict
    {
        file_name: "filename.ext",
        content: "data:image/jpeg;base64,base64 encoded file",
    }
    and store it in memory
    """

    def clean_file(self, data):
        if "content" not in data or "file_name" not in data:
            return None

        filedata = data["content"]
        file_name = data["file_name"]

        if not filedata.startswith("data:"):
            raise ValidationError("waiting after data: json form field")

        header = filedata.split(",")[0]
        content_type = header.split(";")[0]
        base = header.split(";")[1]
        if base != "base64":
            raise ValidationError(f"Wrong encoding for JsonFileField {base}")

        content = base64.b64decode(filedata.split(",")[1])

        file = BytesIO(content)
        file.seek(0)

        filedata = InMemoryUploadedFile(
            file=file,
            field_name="JsonFileField",
            name=file_name,
            content_type=content_type,
            size=len(content),
            charset="utf-8",
        )

        return filedata

    # TODO use clamav to filter virus : https://xael.org/pages/pyclamd-en.html
    def clean(self, data, initial=None):
        if not self.required and data is None:
            return None
        return self.clean_file(data)


class MultipleJsonFileField(JsonFileField):
    def clean(self, data, initial=None):
        if self.required and not data:
            raise ValidationError(_("Un document est requis"))
        if not data:
            return []
        if {} in data:
            raise ValidationError(_("Un document n'est pas fourni"))
        files = []
        for document in data:
            files.append(self.clean_file(document))
        return files


class ListOfValuesField(forms.Field):
    def __init__(self, base_field=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.base_field = base_field
        self.value_list = []

    def clean(self, data):
        if not data:
            raise forms.ValidationError("Enter at least one value.")
        self.value_list = []
        if self.base_field is not None:
            base_field = self.base_field()
            for value in data:
                self.value_list.append(base_field.clean(value))

        return self.value_list

    def get_list(self):
        return self.value_list


class FullModelMultipleChoiceField(forms.ModelMultipleChoiceField):
    """
    Allow to use a form with full multiple objects returned by the frontend

    >>> assignments = FullModelMultipleChoiceField(
    >>>     queryset=AssignmentTag.objects.filter(is_active=True),
    >>>     required=False,
    >>>     to_field_name="pk",
    >>> )
    """

    def prepare_value(self, value):
        if (
            hasattr(value, "__iter__")
            and not isinstance(value, str)
            and not hasattr(value, "_meta")
        ):
            prepare_value = super().prepare_value
            return [prepare_value(v[self.to_field_name]) for v in value]

        return super().prepare_value(value)


class FullModelChoiceField(forms.ModelChoiceField):
    """
    Allow to use a form with a full object returned by the frontend

    >>> referent = FullModelChoiceField(
    >>>     queryset=User.objects.all(), required=True, to_field_name="pk",
    >>> )
    """

    def to_python(self, value):
        if value in self.empty_values:
            return None
        try:
            key = self.to_field_name or "pk"
            if isinstance(value, self.queryset.model):
                value = getattr(value, key)
            value = self.queryset.get(**{key: value[key]})
        except (ValueError, TypeError, self.queryset.model.DoesNotExist):
            raise ValidationError(
                self.error_messages["invalid_choice"], code="invalid_choice"
            )
        return value

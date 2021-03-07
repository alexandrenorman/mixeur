# -*- coding: utf-8 -*-

from typing import List

from helpers.json import camel_to_snakecase

from .models import CustomForm


"""
from fac.models import Contact
from custom_forms.helpers import AnalyzeCustomForm
d=Contact.objects.all().order_by('updated_at').last()
a=AnalyzeCustomForm(obj=d)
a.invalid_fields


from fac.models import Contact
from custom_forms.helpers import AnalyzeCustomForm
d=Contact.objects.get(pk=18589)
a=AnalyzeCustomForm(obj=d)
a.invalid_fields

"""


class AnalyzeCustomForm:
    def __init__(self, obj):
        self.obj = obj

    @property
    def custom_form_data(self) -> dict:
        return self.obj.custom_form_data

    @property
    def invalid_fields(self) -> dict:
        """
        return a dict of invalid fields according to CustomForm validation
        such as { fied_id: label }
        """
        invalid_fields = {}
        for custom_form in self._required_custom_forms:
            invalid_fields = {
                **invalid_fields,
                **self._invalid_fields_for_custom_form(custom_form),
            }

        return invalid_fields

    def _get_custom_form_or_none(self, **data):
        try:
            cf = CustomForm.objects.get(**data)
        except CustomForm.DoesNotExist:
            return None

        return cf

    @property
    def _required_custom_forms(self):
        custom_forms = self._registered_custom_forms
        model = self.obj.__class__.__name__

        # en fait, non on regarde que les contacts et les organizations
        # pour group, project et folder
        # les folders / projects en découle

        anchors = ["Informations"]

        if model in ["Contact", "Organization"]:
            action_models = []
            folder_models = [x.model.pk for x in self.obj.folders.all()]
            group = self.obj.owning_group.pk
            projects = [x.model.project.pk for x in self.obj.folders.all()]

        if model in ["Action"]:
            action_models = [self.obj.model.pk]
            folder_models = []
            group = self.obj.owning_group.pk
            projects = []

        if model in ["Folder"]:
            action_models = []
            folder_models = [self.obj.model.pk]
            group = self.obj.owning_group.pk
            projects = []

        cf = self._get_custom_form_or_none(
            model=model,
            anchor="Informations",
            groups__in=[group],
        )
        if cf:
            custom_forms.append(cf)

        for anchor in anchors:
            for folder_model in folder_models:
                custom_forms.append(
                    self._get_custom_form_or_none(
                        model=model,
                        anchor=anchor,
                        folder_models__in=[folder_model],
                    )
                )

            for project in projects:
                custom_forms.append(
                    self._get_custom_form_or_none(
                        model=model,
                        anchor=anchor,
                        projects__in=[project],
                    )
                )

            for action_model in action_models:
                custom_forms.append(
                    self._get_custom_form_or_none(
                        model=model,
                        anchor=anchor,
                        action_models__in=action_model,
                    )
                )

        custom_forms = [x for x in list(set(custom_forms)) if x is not None]
        return custom_forms

    @property
    def _registered_custom_forms(self) -> List:
        """
        Get used Custom
        """
        if (
            self.custom_form_data is None
            or "custom_form_id" not in self.custom_form_data
        ):
            # TBD, no custom_form_id -> go heuristic and update
            return []

        custom_forms = []
        for cid in self.custom_form_data["custom_form_id"]:
            try:
                cf = CustomForm.objects.get(
                    model=cid["model"],
                    anchor=cid["anchor"],
                    version=cid["version"],
                    projects__pk=cid["project"],
                    action_models__pk=cid["action_model"],
                    folder_models__pk=cid["folder_model"],
                    groups__pk=cid["group"],
                )
                custom_forms.append(cf)
            except KeyError:
                print("TDB", cid)
            except CustomForm.DoesNotExist:
                print("TDB - no such CustomForm", cid)

        return custom_forms

    def _invalid_fields_for_custom_form(self, custom_form) -> dict:
        invalid_fields = {}
        for field in self._get_all_fields(custom_form):
            if not self._is_field_valid(field):
                field_name = field["label"]
                field_id = field["id"]
                invalid_fields[field_id] = field_name

        return invalid_fields

    def _get_all_fields(self, custom_form) -> List:
        return self._get_fields_from_form(form=custom_form.form["content"])

    def _get_fields_from_form(self, form):
        fields = []
        for field in form:
            if "id" in field:
                field["id"] = self._convert_id(field["id"])

            if field["type"] in ["Row", "Fieldset"]:
                for cell in field["cells"]:
                    sub_fields = self._get_fields_from_form(form=cell["children"])
                    for x in sub_fields:
                        fields.append(x)
            elif field["type"] in ["HR", "DisplayText"]:
                continue
            else:
                fields.append(field)

        return fields

    def _convert_id(self, name):
        return camel_to_snakecase(name)

    def _is_field_valid(self, field) -> bool:
        field_validation = {
            "Checkbox": self._validate_checkbox,
            "DateField": self._validate_date_field,
            "NumberField": self._validate_number_field,
            "RadioButton": self._validate_radio_button,
            "SelectList": self._validate_select_list,
            "TextArea": self._validate_text_area,
            "TextField": self._validate_text_field,
        }
        return field_validation[field["type"]](field)

    def _validate_checkbox(self, field):
        return self._validate_count_selected(field)

    def _validate_date_field(self, field):
        return self._validate_field_has_value(field)

    def _validate_number_field(self, field):
        if self.custom_form_data is None or field["id"] not in self.custom_form_data:
            if field["mandatory"] and field["mandatory"] is True:
                return False
            else:
                return True
        else:
            try:
                value = float(self.custom_form_data[field["id"]])
            except Exception:
                if field["mandatory"] and field["mandatory"] is True:
                    return False
                else:
                    if self.custom_form_data[field["id"]] is None:
                        return True

                    return False

            if ("minValue" not in field or field["minValue"] <= value) and (
                "maxValue" not in field or value <= field["maxValue"]
            ):
                return True

        return False

    def _validate_radio_button(self, field):
        return self._validate_field_has_value(field)

    def _validate_select_list(self, field):
        return self._validate_count_selected(field)

    def _validate_text_area(self, field):
        return self._validate_field_has_value(field)

    def _validate_text_field(self, field):
        return self._validate_field_has_value(field)

    def _validate_field_has_value(self, field):
        if self.custom_form_data is None or (
            field["mandatory"]
            and field["mandatory"] is True
            and field["id"] not in self.custom_form_data
        ):
            return False

        return True

    def _validate_count_selected(self, field):
        if self.custom_form_data is None or field["id"] not in self.custom_form_data:
            if field["mandatory"]:
                return False
            else:
                return True
        else:
            if (
                "minChoices" not in field
                or field["minChoices"] <= len(self.custom_form_data[field["id"]])
            ) and (
                "maxChoices" not in field
                or field["maxChoices"] <= len(self.custom_form_data[field["id"]])
            ):
                return True

        return False

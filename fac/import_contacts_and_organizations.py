# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.utils.html import strip_tags
import pandas as pd
from datetime import datetime

from fac.models import FileImport, Organization


from fac.forms import (
    ContactForm,
    OrganizationForm,
    NoteOrganizationForm,
    MemberOfOrganizationForm,
)

from .static_data import TYPE_OF_ORGANIZATION, CIVILITIES


class ImportOrganizationForm(OrganizationForm):
    def __init__(self, *args, **kwargs):
        super(forms.ModelForm, self).__init__(*args, **kwargs)


class ImportContactForm(ContactForm):
    def __init__(self, *args, **kwargs):
        super(forms.ModelForm, self).__init__(*args, **kwargs)


class ImportNoteOrganizationForm(NoteOrganizationForm):
    def __init__(self, *args, **kwargs):
        super(forms.ModelForm, self).__init__(*args, **kwargs)


class ImportMemberOfOrganizationForm(MemberOfOrganizationForm):
    def __init__(self, *args, **kwargs):
        super(forms.ModelForm, self).__init__(*args, **kwargs)


class IncorrectFileError(Exception):
    """
    Exception raised when given file is incorrect

    Attributes:
      filename -- name of file
      message -- explanation of the error
    """

    def __init__(self, filename, message):
        super(IncorrectFileError, self).__init__(message)
        self.filename = filename
        self.message = message


def __get_date_or_now__(data, key):
    return data.get(key) or datetime.now()


def __get_value__(data, key):
    return str(data.get(key) or "").strip()


def __get_type_of_organization__(data, key):
    data = str(data.get(key) or "UNKNOWN").strip()
    if data in [x[0] for x in TYPE_OF_ORGANIZATION]:
        return data

    return "UNKNOWN"


def __get_civility__(data, key):
    data = str(data.get(key) or "-").strip()
    if data in [x[0] for x in CIVILITIES]:
        return data

    return "-"


def __get_bool_default_true__(data, key):
    data = str(data.get(key) or "true").strip()
    if data.lower() in ("1", "y", "o", "oui", "yes", "x", "true"):
        return True
    if data.lower() in ("0", "n", "non", "no", "false"):
        return False
    return True


organization_columns = {
    "type_of_organization": {
        "field": "type_of_organization",
        "method": __get_type_of_organization__,
    },
    "name": {"field": "name", "method": __get_value__},
    "address1": {"field": "address1", "method": __get_value__},
    "address2": {"field": "address2", "method": __get_value__},
    "address3": {"field": "address3", "method": __get_value__},
    "zipcode": {"field": "zipcode", "method": __get_value__},
    "town": {"field": "town", "method": __get_value__},
    "country": {"field": "country", "method": __get_value__},
    "email": {"field": "email", "method": __get_value__},
    "website": {"field": "website", "method": __get_value__},
    "phone": {"field": "phone", "method": __get_value__},
    "fax": {"field": "fax", "method": __get_value__},
    "tags": {"field": "tags", "method": __get_value__},
    "referent": {"field": "referent", "method": __get_value__},
    "created_at": {"field": "created_at", "method": __get_date_or_now__},
}

contact_columns = {
    "contact_civility": {"field": "civility", "method": __get_civility__},
    "contact_firstname": {"field": "firstname", "method": __get_value__},
    "contact_lastname": {"field": "lastname", "method": __get_value__},
    "contact_email": {"field": "email", "method": __get_value__},
    "contact_address1": {"field": "address1", "method": __get_value__},
    "contact_address2": {"field": "address2", "method": __get_value__},
    "contact_zipcode": {"field": "zipcode", "method": __get_value__},
    "contact_town": {"field": "town", "method": __get_value__},
    "contact_country": {"field": "country", "method": __get_value__},
    "contact_phone": {"field": "phone", "method": __get_value__},
    "contact_mobile_phone": {"field": "mobile_phone", "method": __get_value__},
    "contact_fax": {"field": "fax", "method": __get_value__},
    "contact_tags": {"field": "tags", "method": __get_value__},
    "created_at": {"field": "created_at", "method": __get_date_or_now__},
    "contact_title_in_organization": {
        "field": "title_in_organization",
        "method": __get_value__,
    },
    "contact_use_address_from_organization": {
        "field": "use_address_from_organization",
        "method": __get_bool_default_true__,
    },
}


def import_contacts_and_organizations(file_import_pk, imported_file):  # NOQA: C901
    """
    import given file and transform result to
    Contacts, Organizations and MemberOfOrganizations

    use with:
    from django.db import transaction
    with transaction.atomic():

    Parameters:
      file_import_pk -- pk of related FileImport object
      imported_file -- FileField containing the file to import
    """

    errors = []
    file_import = FileImport.objects.get(pk=file_import_pk)

    data = pd.read_csv(imported_file, keep_default_na=False)
    line_number = 1
    other_keys = []
    for d in data.iterrows():
        if line_number == 1:
            columns_searched = list(organization_columns) + list(contact_columns)
            columns_found = []
            for k in d[1].keys():
                if k not in columns_searched:
                    other_keys.append(k)
                else:
                    columns_found.append(k)

            file_import.columns_found = ", ".join(columns_found)
            file_import.columns_not_found = ", ".join(
                [x for x in columns_searched if x not in columns_found]
            )
            file_import.columns_not_used = ", ".join(other_keys)
            file_import.save()

        line_number += 1

        created_org = None

        odata = {"fileimport": file_import_pk}
        for key in organization_columns:
            odata[organization_columns[key]["field"]] = organization_columns[key][
                "method"
            ](d[1], key)

        # create Organization is odata['name'] is not empty
        if odata["name"]:
            if Organization.objects.filter(name=odata["name"]).count() == 0:
                organization_form = ImportOrganizationForm(odata)
                if organization_form.is_valid():
                    created_org = organization_form.save()

                    if other_keys:
                        note = []
                        for k in other_keys:
                            n = str(d[1].get(k) or "").strip()
                            if n:
                                note.append("{}: {}".format(k, n))

                        ndata = {
                            "created_at": odata["created_at"],
                            "organization": created_org.pk,
                            "note": "\n".join(note),
                            "tags": "Import",
                        }
                        org_note_form = ImportNoteOrganizationForm(ndata)
                        if org_note_form.is_valid():
                            org_note_form.save()
                        else:
                            msgs = [
                                "{}: {}".format(
                                    x, strip_tags(str(org_note_form.errors[x]))
                                )
                                for x in org_note_form.errors.keys()
                            ]
                            for msg in msgs:
                                errors.append(
                                    _("Ligne:{} : Erreur avec la note {} [{}]").format(
                                        line_number, odata["name"], msg
                                    )
                                )

                else:
                    msgs = [
                        "{}: {}".format(x, strip_tags(str(organization_form.errors[x])))
                        for x in organization_form.errors.keys()
                    ]
                    for msg in msgs:
                        errors.append(
                            _("Ligne:{} : Erreur avec l'organisation {} [{}]").format(
                                line_number, odata["name"], msg
                            )
                        )
            else:
                created_org = Organization.objects.get(name=odata["name"])

        cdata = {"phplist_subscriber_id": 0, "fileimport": file_import_pk}
        for key in contact_columns:
            cdata[contact_columns[key]["field"]] = contact_columns[key]["method"](
                d[1], key
            )

        # create Contact
        created_contact = None
        if cdata["firstname"] or cdata["lastname"] or cdata["email"]:
            contact_form = ImportContactForm(cdata)
            if contact_form.is_valid():
                created_contact = contact_form.save()
            else:
                msgs = [
                    "{}: {}".format(x, strip_tags(str(contact_form.errors[x])))
                    for x in contact_form.errors.keys()
                ]
                for msg in msgs:
                    errors.append(
                        _("Ligne:{} : Erreur avec le contact {} [{}]").format(
                            line_number,
                            "{} {} {}".format(
                                cdata["firstname"], cdata["lastname"], cdata["email"]
                            ),
                            msg,
                        )
                    )

            # if Organization was created, create MemberOfOrganization
            if created_org and created_contact:
                moodata = {
                    "contact": created_contact.pk,
                    "organization": created_org.pk,
                    "use_address_from_organization": cdata[
                        "use_address_from_organization"
                    ],
                    "title_in_organization": cdata["title_in_organization"],
                    "created_at": cdata["created_at"],
                }
                moo_form = ImportMemberOfOrganizationForm(moodata)
                if moo_form.is_valid():
                    moo_form.save()
                else:
                    msgs = [
                        "{}: {}".format(x, strip_tags(str(moo_form.errors[x])))
                        for x in moo_form.errors.keys()
                    ]
                    for msg in msgs:
                        errors.append(
                            _(
                                "Ligne:{} : Erreur avec l'appartenance du contact à une organisation {} [{}]"
                            ).format(line_number, odata["name"], msg)
                        )

    if errors:
        raise IncorrectFileError(filename=imported_file, message=errors)
    return

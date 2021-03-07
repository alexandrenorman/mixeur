# -*- coding: utf-8 -*-
from custom_forms.helpers import AnalyzeCustomForm

from fac.models import Contact, Organization, Project


def _is_empty(value, min_length=1):
    if not value:
        return True
    if value.__class__.__name__ == "ManyRelatedManager":
        return len(value.all()) < min_length
    return len(value) < min_length


def get_obj_requirements(obj, requirements_names):
    requirements = {}
    for folder in obj.folders.all():
        for (requirement_name, requirement_field_name) in requirements_names.items():
            requirements[requirement_name] = requirements.get(
                requirement_name, False
            ) or getattr(folder.model.project, requirement_field_name)
    return {
        requirement_name[: -len("_mandatory")]  # noqa: E203
        for requirement_name, requirement_value in requirements.items()
        if requirement_value
    }


def get_incomplete_contacts(contacts):
    incomplete_contacts = []
    contact_requirements_names = Project.get_contact_field_requirements()

    for contact in contacts:
        incomplete_fields = get_incomplete_fields_for_contact(
            contact, contact_requirements_names
        )

        if incomplete_fields:
            contact.incomplete_fields = incomplete_fields
            incomplete_contacts.append(contact)

    return incomplete_contacts


def get_incomplete_fields_for_contact(contact, contact_requirements_names=None):
    contact_requirements_names = (
        contact_requirements_names or Project.get_contact_field_requirements()
    )
    incomplete_fields = get_incomplete_custom_forms_fields(contact)

    for attribute in get_obj_requirements(contact, contact_requirements_names):
        if _is_empty(getattr(contact, attribute)):
            incomplete_fields.append(
                Contact._meta.get_field(attribute).verbose_name.title()
            )

    for member_of_organization in contact.memberoforganization_set.all():
        organization = member_of_organization.organization
        if organization.folders.filter(
            model__project__should_members_of_organization_respect_rules=True
        ).exists():
            for attribute in get_obj_requirements(
                organization, contact_requirements_names
            ):
                if _is_empty(getattr(contact, attribute)):
                    incomplete_fields.append(
                        Contact._meta.get_field(attribute).verbose_name.title()
                    )

    if not (contact.email or contact.phone or contact.mobile_phone):
        incomplete_fields.append("Courriel/Téléphone")

    return incomplete_fields


def get_incomplete_organizations(organizations):
    incomplete_organizations = []
    orga_requirements_names = Project.get_organization_field_requirements()

    for organization in organizations:
        incomplete_fields = get_incomplete_fields_for_organization(
            organization, orga_requirements_names
        )

        if incomplete_fields:
            organization.incomplete_fields = incomplete_fields
            incomplete_organizations.append(organization)

        if not (organization.email or organization.phone):
            incomplete_fields.append("Courriel/Téléphone")

    return incomplete_organizations


def get_incomplete_fields_for_organization(organization, orga_requirements_names=None):
    orga_requirements_names = (
        orga_requirements_names or Project.get_organization_field_requirements()
    )
    incomplete_fields = get_incomplete_custom_forms_fields(organization)

    for attribute in get_obj_requirements(organization, orga_requirements_names):
        min_length = 1
        if attribute == "description":
            min_length = 10
        if _is_empty(getattr(organization, attribute), min_length):
            incomplete_fields.append(
                Organization._meta.get_field(attribute).verbose_name.title()
            )

    return incomplete_fields


def get_incomplete_custom_forms_fields(obj):
    incomplete_fields = AnalyzeCustomForm(obj).invalid_fields
    return [incomplete_fields[x] for x in incomplete_fields]

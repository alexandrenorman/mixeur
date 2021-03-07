import serpy

from fac.models import Project

from .contact_serializer import ContactSerializer


def get_obj_requirements(obj, requirements_names):
    requirements = {}
    for folder in obj.folders.all():
        for (requirement_name, requirement_field_name) in requirements_names.items():
            requirements[requirement_name] = requirements.get(
                requirement_name, False
            ) or getattr(folder.model.project, requirement_field_name)
    return requirements


class ContactEditSerializer(ContactSerializer):
    client_account = serpy.MethodField()
    requirements = serpy.MethodField()

    def get_client_account(self, contact):
        if contact.client_account:
            return contact.client_account.pk

    def get_requirements(self, contact):
        requirements_names = Project.get_contact_field_requirements()
        requirements = {}

        requirements.update(get_obj_requirements(contact, requirements_names))
        for member_of_organization in contact.memberoforganization_set.all():
            organization = member_of_organization.organization
            if organization.folders.filter(
                model__project__should_members_of_organization_respect_rules=True
            ).exists():
                requirements.update(
                    get_obj_requirements(organization, requirements_names)
                )

        return requirements

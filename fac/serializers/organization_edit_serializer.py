from fac.models import Project
from .organization_serializer import OrganizationSerializer


class OrganizationEditSerializer(OrganizationSerializer):
    def get_requirements(self, organization):
        requirements_names = Project.get_organization_field_requirements()
        requirements = {}
        for folder in organization.folders.all().prefetch_related("model__project"):
            for (
                requirement_name,
                requirement_field_name,
            ) in requirements_names.items():
                requirements[requirement_name] = requirements.get(
                    requirement_name, False
                ) or getattr(folder.model.project, requirement_field_name)
        return requirements

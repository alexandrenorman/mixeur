import serpy

from fac.models import Project
from .folder_model_simple_serializer import FolderModelSimpleSerializer
from .category_model_serializer import CategoryModelSerializer


class FolderModelSerializer(FolderModelSimpleSerializer):
    exclude = ["icon_marker"]

    categories = serpy.MethodField()

    def get_categories(self, folder_model):
        return CategoryModelSerializer(folder_model.categories.all(), many=True).data

    def get_project(self, folder_model):
        return folder_model.project.pk

    def get_organization_requirements(self, folder_model):
        requirements_names = Project.get_organization_field_requirements()
        requirements = {}
        for (requirement_name, requirement_field_name) in requirements_names.items():
            requirements[requirement_name] = requirements.get(
                requirement_name, False
            ) or getattr(folder_model.project, requirement_field_name)
        return requirements

    def get_contact_requirements(self, folder_model):
        requirements_names = Project.get_contact_field_requirements()
        requirements = {}
        for (requirement_name, requirement_field_name) in requirements_names.items():
            requirements[requirement_name] = requirements.get(
                requirement_name, False
            ) or getattr(folder_model.project, requirement_field_name)
        return requirements

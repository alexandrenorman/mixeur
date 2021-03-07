from .contact_serializer import ContactSerializer


class ContactIconSerializer(ContactSerializer):
    def get_folders_project(self, obj):
        projects = {folder.model.project for folder in obj.folders.all()}
        return [{"label": project.name, "value": project.pk} for project in projects]

    def get_folders_status(self, obj):
        statuses = []
        for folder in obj.folders.all():
            status = folder.get_status()
            if not status:
                continue
            statuses.append(
                {
                    "color": status.color,
                    "icon": folder.model.icon_marker_content,
                    "folder": folder.pk,
                    "project": folder.model.project.pk,
                    "status": status.name,
                    "order": status.order,
                }
            )
        return statuses

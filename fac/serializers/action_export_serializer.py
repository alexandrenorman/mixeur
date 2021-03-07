from os.path import basename

import serpy


class ActionExportSerializer(serpy.Serializer):
    name = serpy.MethodField()
    document = serpy.MethodField()
    duration = serpy.MethodField()
    organization_pk = serpy.MethodField()
    contact_pk = serpy.MethodField()
    linked_object_type = serpy.MethodField()
    group = serpy.MethodField()
    date = serpy.MethodField()
    contact = serpy.MethodField()
    message = serpy.MethodField()
    remote = serpy.MethodField()
    done_by = serpy.MethodField()

    def get_done_by(self, action):
        try:
            done_by = action.done_by.full_name
        except AttributeError:
            done_by = ""

        return done_by

    def get_name(self, action):
        return action.model.name

    def get_document(self, action):
        return ", ".join(basename(f.document.name) for f in action.files.all())

    def get_duration(self, action):
        return action.duration or None

    def get_organization_pk(self, action):
        if (
            not action.folder.content_type
            or action.folder.content_type.model == "contact"
        ):
            return -1

        return action.folder.object_id

    def get_contact_pk(self, action):
        if (
            not action.folder.content_type
            or action.folder.content_type.model == "organization"
        ):
            return -1

        return action.folder.object_id

    def get_linked_object_type(self, action):
        if action.folder.content_type:
            return action.folder.content_type.model

    def get_group(self, action):
        return f"{action.folder.owning_group}"

    def get_date(self, action):
        return action.date

    def get_contact(self, action):
        if not action.contact:
            return {}

        return {
            "name": f"{action.contact.last_name} {action.contact.first_name}",
            "pk": action.contact.pk,
        }

    def get_message(self, action):
        return action.message

    def get_remote(self, action):
        return len([tag for tag in action.tags.all() if tag.name == "À distance"]) > 0

    def get_custom_form_data(self, obj):
        if obj.custom_form_data is None:
            return {}

        return obj.custom_form_data

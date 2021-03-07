# -*- coding: utf-8 -*-
import csv
import io

from fac.models import Contact


class ListCSVSerializer:
    def __init__(self, objects, *args, **kwargs):
        self.object = objects  # We can have a single list or a list of List

    @property
    def data(self):
        csv_fh = io.StringIO()
        csv_writer = csv.writer(csv_fh, delimiter=";")
        csv_writer.writerow(
            [
                # https://en.wikipedia.org/wiki/Byte_order_mark
                "\ufeffNom",
                "Prénom",
                "Courriel",
                "Accepte de recevoir des newsletters",
                "Téléphone",
                "Tags",
            ]
        )

        if isinstance(self.object, list):
            not_duplicated_contacts = set()
            for li in self.object:
                contacts = self.fill_csv_with_contacts(csv_writer, li.get_contacts())
                for contact in contacts:
                    not_duplicated_contacts.add(contact)
            self.fill_csv_with_contacts(csv_writer, not_duplicated_contacts)
        else:
            self.fill_csv_with_contacts(csv_writer, self.object.get_contacts())
        csv_fh.seek(0)
        return {"csv": csv_fh.read()}

    def fill_csv_with_contacts(self, csv_writer, contacts):
        for contact in contacts:
            csv_writer.writerow(
                [
                    contact.last_name if isinstance(contact, Contact) else contact.name,
                    contact.first_name if isinstance(contact, Contact) else "",
                    contact.email,
                    "Oui" if contact.accepts_newsletters else "Non",
                    contact.phone,
                    ",".join(tag.name for tag in contact.tags.all()),
                ]
            )

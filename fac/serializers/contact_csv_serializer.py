import csv
import io


class ContactCSVSerializer:
    def __init__(self, contacts, *args, **kwargs):
        self.contacts = contacts

    @property
    def data(self):
        csv_fh = io.StringIO()
        # delimiter=";" because excel.
        csv_writer = csv.writer(csv_fh, delimiter=";")
        csv_writer.writerow(
            [
                # https://en.wikipedia.org/wiki/Byte_order_mark
                "\ufeffCivilité",
                "Prénom",
                "Nom",
                "Courriel",
                "Accepte de recevoir des newsletters",
                "Adresse",
                "Code postal",
                "Ville",
                "Pays",
                "Téléphone",
                "Mobile",
                "Tags",
                "Structure",
                "Titre",
            ]
        )

        for contact in self.contacts:
            member = contact.memberoforganization_set.first()
            csv_writer.writerow(
                [
                    contact.civility,
                    contact.first_name,
                    contact.last_name,
                    contact.email,
                    "Oui" if contact.accepts_newsletters else "Non",
                    contact.address,
                    contact.zipcode,
                    contact.town,
                    contact.country,
                    contact.phone_cache,
                    contact.mobile_phone_cache,
                    ",".join(tag.name for tag in contact.tags.all()),
                    member.organization.name if member else "",
                    member.title_in_organization if member else "",
                ]
            )
        csv_fh.seek(0)
        return {"csv": csv_fh.read()}

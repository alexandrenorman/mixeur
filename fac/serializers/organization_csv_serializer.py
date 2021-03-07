import csv
import io


class OrganizationCSVSerializer:
    def __init__(self, organizations, *args, **kwargs):
        self.organizations = organizations

    @property
    def data(self):
        csv_fh = io.StringIO()
        # delimiter=";" because excel.
        csv_writer = csv.writer(csv_fh, delimiter=";")
        csv_writer.writerow(
            [
                # https://en.wikipedia.org/wiki/Byte_order_mark
                "\ufeffNom",
                "Description",
                "Référence interne",
                "Type de structure",
                "Adresse",
                "Code postal",
                "Ville",
                "Pays",
                "Courriel",
                "Accepte de recevoir des newsletters",
                "Site",
                "Téléphone",
                "Tags",
                "Referents",
            ]
        )

        for organization in self.organizations:
            csv_writer.writerow(
                [
                    organization.name,
                    organization.description,
                    organization.reference,
                    organization.type_of_organization,
                    organization.address,
                    organization.zipcode,
                    organization.town,
                    organization.country,
                    organization.email,
                    "Oui" if organization.accepts_newsletters else "Non",
                    organization.website,
                    organization.phone_cache,
                    ",".join(tag.name for tag in organization.tags.all()),
                    ",".join(user.email for user in organization.referents.all()),
                ]
            )
        csv_fh.seek(0)
        return {"csv": csv_fh.read()}

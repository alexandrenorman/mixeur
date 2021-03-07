from django.core.management.base import BaseCommand

from fac.models import Contact, Organization, NoteOrganization, MemberOfOrganization

import csv


# addr = google_v3(self.address)
# self.latitude = addr.latitude
# self.longitude = addr.longitude
# self.address_normalized = addr.address


class Command(BaseCommand):
    help = "Import organizations and contacts from CSV file."

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument("source", nargs="+", type=str)

        # Named (optional) arguments
        parser.add_argument(
            "--source",
            action="store_true",
            dest="source",
            default=None,
            help="source file",
        )

    def handle(self, *args, **options):  # NOQA: C901

        if options["source"]:
            for o in MemberOfOrganization.objects.all():
                o.delete()
            for o in Organization.objects.all():
                o.delete()
            for o in Contact.objects.all():
                o.delete()

            with open(options["source"][0], "r", encoding="utf-8") as fsource:
                spamreader = csv.reader(fsource, delimiter=",", quotechar='"')

                for row in spamreader:
                    (
                        numero,
                        date_de_saisie,
                        type_de_prospect,
                        structure_mere,
                        nom_structure,
                        site_internet,
                        adresse1,
                        code_postal,
                        ville,
                        pays,
                        email_entreprise,
                        telephone_entreprise,
                        contact,
                        fonction,
                        telephone,
                        email_contact,
                        tags,
                        nbr_installations,
                        p_totale,
                        production,
                        commentaires,
                        source,
                        referent,
                    ) = row
                    try:
                        numero = int(numero)
                    except ValueError:
                        continue

                    orga = Organization.objects.create(
                        type_of_organization="Company",
                        name=nom_structure,
                        email=email_entreprise,
                        website=site_internet,
                        address1=adresse1,
                        address2="",
                        address3="",
                        zipcode=code_postal,
                        town=ville,
                        country=pays,
                        phone=telephone_entreprise,
                        fax="",
                        tags="",
                    )
                    orga.save()

                    note = """structure mere : {}
date de saisie : {}
nbr installations: {}
P totale : {}
Production : {}

Commentaire : {}
""".format(
                        structure_mere,
                        date_de_saisie,
                        nbr_installations,
                        p_totale,
                        production,
                        commentaires,
                    )

                    NoteOrganization.objects.create(organization=orga, note=note)

                    for tag in type_de_prospect.split(","):
                        if len(tag.strip()) > 0:
                            orga.tags.add(tag.strip().lower())

                    for tag in tags.split(","):
                        if len(tag.strip()) > 0:
                            orga.tags.add(tag.strip().lower())

                    if len(referent) > 0:
                        orga.tags.add(referent.strip().lower())
                    if len(source) > 0:
                        orga.tags.add(source.strip().lower())

                    orga.save()

                    if len(contact + email_contact) > 0:
                        lastname = contact.strip().split(" ")[-1]
                        firstname = " ".join(contact.strip().split(" ")[:-1])

                        # Try to guess if lastname and firstname are inverted
                        if firstname.upper() == firstname:
                            firstname, lastname = lastname, firstname

                        tcontact = Contact.objects.create(
                            firstname=firstname,
                            lastname=lastname,
                            phone=telephone,
                            email=email_contact,
                        )
                        tcontact.save()

                        # contact, fonction,
                        # telephone, email

                        moo = MemberOfOrganization.objects.create(
                            contact=tcontact,
                            organization=orga,
                            title_in_organization=fonction,
                        )
                        moo.save()

        return

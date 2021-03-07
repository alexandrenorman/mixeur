import csv
import io
import logging
import traceback

import requests
from attr import dataclass
from django.db import transaction
from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.http import require_http_methods

from accounts.models import Group, User
from fac.models import Tag, Contact, Organization, MemberOfOrganization
from fac.static_data import CIVILITIES, TYPE_OF_ORGANIZATION

logger = logging.getLogger(__name__)


@dataclass(init=False)
class CsvOrganization:
    name: str
    referent_email: str
    reference: str
    type_of_organization: str
    address: str
    zipcode: str
    town: str
    country: str
    email: str
    website: str
    phone: str
    tags: [str]
    line_nb: int
    lat: float = 0.0
    lon: float = 0.0

    def __init__(self, row, line_nb):
        # if the row does not have enough columns, artificially add them
        number_of_fields = 13
        row += ["" for _ in range(number_of_fields - len(row))]
        self.line_nb = line_nb
        self.name = row[0]
        self.referent_email = row[1]
        self.reference = row[2]
        type_of_organization = row[3].replace("Agence Immo", "Agence Immobilière")
        matching_type = [
            available_type[0]
            for available_type in TYPE_OF_ORGANIZATION
            if available_type[1] == type_of_organization
        ] or ["UNKNOWN"]
        self.type_of_organization = matching_type[0]
        self.address = row[4]
        self.zipcode = row[5]
        self.town = row[6]
        self.country = row[7]
        self.email = row[8]
        self.website = row[9]
        self.phone = row[10]
        if row[11]:
            self.tags = row[11].split(",")
        else:
            self.tags = []
        if row[12]:
            self.tags.append(row[12])
        self.lat = 0.0
        self.lon = 0.0

    def set_lat_lon(self, lat, lon):
        try:
            self.lat = float(lat) or 0.0
            self.lon = float(lon) or 0.0
        except ValueError:
            self.lat = self.lon = 0.0


@dataclass(init=False)
class CsvContact:
    civility: str
    first_name: str
    last_name: str
    email: str
    address: str
    zipcode: str
    town: str
    country: str
    phone: str
    mobile_phone: str
    tags: [str]
    organization: str
    title: str
    referent_email: str
    line_nb: int
    lat: float = 0.0
    lon: float = 0.0

    def __init__(self, row, line_nb):
        # if the row does not have enough columns, artificially add them
        number_of_fields = 14
        row += ["" for _ in range(number_of_fields - len(row))]
        self.line_nb = line_nb
        self.civility = row[0]
        if self.civility == "Mlle":
            self.civility = "Mme"
        elif not [c for c in CIVILITIES if c[0] == self.civility]:
            self.civility = "-"
        self.first_name = row[1]
        self.last_name = row[2]
        self.email = row[3]
        self.address = row[4]
        self.zipcode = row[5]
        self.town = row[6]
        self.country = row[7]
        self.phone = row[8]
        self.mobile_phone = row[9]
        if row[10]:
            self.tags = row[10].split(",")
        else:
            self.tags = []
        self.organization = row[11]
        self.title = row[12]
        self.referent_email = row[13]
        self.lat = 0.0
        self.lon = 0.0

    def set_lat_lon(self, lat, lon):
        try:
            self.lat = float(lat) or 0.0
            self.lon = float(lon) or 0.0
        except ValueError:
            self.lat = self.lon = 0.0


def _clean_header(header):
    """
    The headers look a bit random, we use this method to homogeneise them
    :header: the orinal header
    :return: a simplified form of the header
    """
    return (
        header.strip(",")
        .replace(" de la structure", "")
        .replace("facultatif", "optionnel")
        .replace(" (optionnel)", "")
        .replace(" (optionnels)", "")
        .replace("Téléphone(format0123456789)", "Téléphone (format 0123456789)")
        .replace("Pays ", "Pays")
        .replace("Structure associée", "Structure")
        .replace(",Titre,", ",Titre/fonction dans la structure,")
    )


def cleanup_files(files):
    csv_file_object = files["organizations"]
    with csv_file_object.open() as csv_file_handler:
        csv_organizations = csv_file_handler.read().decode().strip()

    # cleanup file from non-ascii characters
    csv_organizations = "".join(
        filter(lambda c: ord(c) < 256 or c == "’", csv_organizations)
    )

    header_organizations = _clean_header(csv_organizations.split("\n")[0])

    expected_header_organizations = _clean_header(
        "Nom,Référent interne - merci de saisir une adresse email "
        "liée à un compte Mixeur existant,Référence interne (optionnel),"
        "Type de structure,Adresse,Code postal,Ville,Pays,Courriel (optionnel),"
        "Site (optionnel),Téléphone (format 0123456789) (optionnel),"
        "Tags (optionnels),Tag obligatoire"
    )
    if not header_organizations.startswith(expected_header_organizations):
        raise Exception(
            _(
                "La ligne d'entête des Structures ne correspond pas à celle attendue,"
                "le format du fichier d'import a peut-être changé ?"
                "\n\n"
                f"Attendu : {expected_header_organizations}\n"
                f"Reçu : {header_organizations}\n"
            )
        )

    lines_organizations = csv_organizations.split("\n")[1:]
    # remove empty lines
    lines_organizations = [
        line for line in lines_organizations if set(line) and set(line) != {","}
    ]
    organizations_csv = "\n".join([expected_header_organizations] + lines_organizations)

    # Contact
    csv_file_object = files.get("contacts")
    if not csv_file_object:
        return io.StringIO(organizations_csv), None

    with csv_file_object.open() as csv_file_handler:
        csv_contacts = csv_file_handler.read().decode().strip()

    # cleanup file from non-ascii characters
    csv_contacts = "".join(filter(lambda c: ord(c) < 256, csv_contacts))
    header_contacts = _clean_header(csv_contacts.split("\n")[0])
    expected_header_contacts = _clean_header(
        "Civilité,Prénom,Nom,Courriel,Adresse (optionnel),Code postal (optionnel),"
        "Ville (optionnel),Pays (optionnel) ,Téléphone (optionnel),Mobile (optionnel),"
        "Tags (optionnel),Structure associée,Titre/fonction dans la structure,"
        "Référent interne (optionnel) "
        "- merci de saisir une adresse email liée à un compte Mixeur existant"
    )
    if not header_contacts.startswith(expected_header_contacts):
        raise Exception(
            _(
                "La ligne d'entête des Contacts ne correspond pas à celle attendue,"
                "le format du fichier d'import a peut-être changé ?"
                "\n\n"
                f"Attendu : {expected_header_contacts}\n"
                f"Reçu : {header_contacts}\n"
            )
        )
    lines_contacts = csv_contacts.split("\n")[1:]

    # remove empty lines
    lines_contacts = [
        line for line in lines_contacts if set(line) and set(line) != {","}
    ]

    contacts_csv = "\n".join([expected_header_organizations] + lines_contacts)

    return io.StringIO(organizations_csv), io.StringIO(contacts_csv)


def _add_lat_lon(organizations_or_contacts_dict):
    # We can send a CSV to the https://geo.api.gouv.fr API
    # It returns the same CSV with additional columns (like latitude/longitude)
    geo_api_csv_header = ["adresse", "postcode"]
    api_gov_url = "https://api-adresse.data.gouv.fr/search/csv/"

    csv_file = io.StringIO()
    geo_api_csv = csv.writer(
        csv_file,
        delimiter=",",
        quotechar='"',
        quoting=csv.QUOTE_MINIMAL,
        lineterminator="\n",
    )
    geo_api_csv.writerow(geo_api_csv_header)
    organizations_or_contacts_list = list(organizations_or_contacts_dict.values())
    for organization_or_contact in organizations_or_contacts_list:
        csv_value = organization_or_contact["csv_value"]
        address = csv_value.address.strip()
        if csv_value.town.strip().lower() not in address.lower():
            address += f" {csv_value.town.strip()}"
        geo_api_csv.writerow([address.strip(), csv_value.zipcode])

    csv_file.seek(0)
    api_response = requests.post(
        api_gov_url,
        files=[
            ("data", ("data", csv_file.read(), "application/octet-stream")),
            ("postcode", (None, "postcode")),
            ("result_columns", (None, "latitude")),
            ("result_columns", (None, "longitude")),
        ],
        timeout=60,
    )
    api_response.raise_for_status()
    with_lat_lon_csv = csv.reader(io.StringIO(api_response.text))

    next(with_lat_lon_csv)  # skip header
    for line_nb, row in enumerate(with_lat_lon_csv):
        if len(row) >= 4:
            organizations_or_contacts_list[line_nb]["csv_value"].set_lat_lon(
                row[2], row[3]
            )


def add_lat_lon(organizations, contacts):
    if organizations:
        _add_lat_lon(organizations)
    if contacts:
        _add_lat_lon(contacts)


def do_import_csv(
    files,
    owning_group_id,
    organizations,
    contacts,
    tags,
    member_of_organizations,
    duplicate_organizations,
    duplicate_contacts,
    already_existing_organizations,
    already_existing_contacts,
    already_existing_tags,
):
    """
    This method:
    - reads the contact and organization CSV
    - checks for pre-existing objects in the database and do NOT try to re-create
      nor update them. Log these entries
    - checks for duplicate lines in the CSV, adds the first line to the DB, then ignores
      the following duplicates and logs them
    - creates the Tags, Organizations, Contacts according to the data in the files
    :files: , the files POSTed
    :owning_group_id: , the pk of the  Group under which we create the objects
    :organizations: , the method fills this dict with the created Organizations
    :contacts: , the method fills this dict with the created Contacts
    :tags: , the method fills this dict with the created Tags
    :member_of_organizations: , the method fills this dict with the created
           MemberOfOrganizations
    :duplicate_organizations: , the method fills this list with the duplicate
           organizations in the organization CSV
    :duplicate_contacts: , the method fills this list with the duplicate contacts
           in the contact CSV
    :already_existing_organizations: , the method fills this list with the
           pre-existing organizations in the DB
    :already_existing_contacts: , the method fills this list with the  pre-existing
           contacts in the DB
    :already_existing_tags: , the method fills this list with the pre-existing
           contacts in the DB
    """
    organizations_file, contacts_file = cleanup_files(files)
    owning_group = Group.objects.get(pk=owning_group_id)

    _parse_organization_csv(
        already_existing_organizations,
        duplicate_organizations,
        organizations,
        organizations_file,
        owning_group,
        tags,
    )

    if contacts_file:
        _parse_contact_csv(
            already_existing_contacts,
            contacts,
            contacts_file,
            duplicate_contacts,
            owning_group,
            tags,
        )

    add_lat_lon(organizations, contacts)

    with transaction.atomic():
        create_objects(
            owning_group,
            already_existing_tags,
            contacts,
            organizations,
            tags,
            member_of_organizations,
        )


def _parse_contact_csv(
    already_existing_contacts,
    contacts,
    contacts_file,
    duplicate_contacts,
    owning_group,
    tags,
):
    contacts_csv_file = csv.reader(contacts_file)
    next(contacts_csv_file)  # skip header
    for line_nb, row in enumerate(contacts_csv_file):
        try:
            contact = CsvContact(row, line_nb + 2)
        except Exception:
            raise Exception(f"CSV contact, ligne {line_nb + 2}")
        ref = (
            f"{contact.first_name}-{contact.last_name}"
            f"-{contact.email}-{contact.address}"
        )

        if ref in contacts:
            # this line is duplicated in the CSV
            duplicate_contacts.append((contact, contacts[ref]["csv_value"]))
            continue
        if Contact.objects.filter(
            last_name__iexact=contact.last_name,
            first_name__iexact=contact.first_name,
            address__iexact=contact.address,
            email=contact.email,
            owning_group=owning_group,
        ).exists():
            # this contact is already in the database
            already_existing_contacts.append(contact)
            continue

        if (
            contact.referent_email
            and not User.objects.filter(
                group=owning_group, email=contact.referent_email
            ).exists()
        ):
            raise Exception(
                "Impossible de trouver l'Utilisateur avec l'email"
                f"{contact.referent_email} dans le groupe {owning_group} "
                f"(CSV contacts, ligne {contact.line_nb})"
            )

        contacts[ref] = {"csv_value": contact}
        for tag in contact.tags:
            tags[tag] = {"csv_value": tag}


def _parse_organization_csv(
    already_existing_organizations,
    duplicate_organizations,
    organizations,
    organizations_file,
    owning_group,
    tags,
):
    organizations_csv_file = csv.reader(organizations_file)
    next(organizations_csv_file)  # skip header
    for line_nb, row in enumerate(organizations_csv_file):
        try:
            organization = CsvOrganization(row, line_nb + 2)
        except Exception:
            raise Exception(f"CSV structures, ligne {line_nb + 2}")
        ref = (
            f"{organization.name}-{organization.type_of_organization}"
            f"-{organization.address}-{organization.town}-{organization.phone}"
        )

        if ref in organizations:
            # this line is duplicated in the CSV
            duplicate_organizations.append(
                (organization, organizations[ref]["csv_value"])
            )
            continue
        if Organization.objects.filter(
            name__iexact=organization.name,
            type_of_organization__iexact=organization.type_of_organization,
            address__iexact=organization.address,
            owning_group=owning_group,
        ).exists():
            # this organization is already in the database
            already_existing_organizations.append(organization)
            continue
        if (
            organization.referent_email
            and not User.objects.filter(
                group=owning_group, email=organization.referent_email
            ).exists()
        ):
            raise Exception(
                "Impossible de trouver l'Utilisateur avec l'email"
                f"{organization.referent_email} dans le groupe {owning_group} "
                f"(CSV structures, ligne {organization.line_nb})"
            )

        organizations[ref] = {"csv_value": organization}
        for tag in organization.tags:
            tags[tag] = {"csv_value": tag}


def create_objects(
    owning_group,
    already_existing_tags,
    contacts,
    organizations,
    tags,
    member_of_organizations,
):
    _create_tags(already_existing_tags, owning_group, tags)
    _create_organizations(organizations, owning_group, tags)
    _create_contacts_and_memberoforganizations(
        contacts, member_of_organizations, owning_group, tags
    )


def _create_tags(already_existing_tags, owning_group, tags):
    for tag in tags.values():
        tag_value = tag["csv_value"]
        db_tag = Tag.objects.filter(
            name__iexact=tag_value, owning_group=owning_group
        ).first()
        if db_tag:
            tags[tag_value]["db_value"] = db_tag
            already_existing_tags.append(tag_value)
            continue
        tags[tag_value]["db_value"] = Tag.objects.create(
            name=tag_value, owning_group=owning_group
        )


def _create_contacts_and_memberoforganizations(
    contacts, member_of_organizations, owning_group, tags
):
    for contact in contacts.values():
        contact_csv = contact["csv_value"]
        try:
            contact_db = Contact.objects.create(
                owning_group=owning_group,
                civility=contact_csv.civility,
                first_name=contact_csv.first_name,
                last_name=contact_csv.last_name,
                email=contact_csv.email,
                address=contact_csv.address,
                zipcode=contact_csv.zipcode,
                town=contact_csv.town,
                country=contact_csv.country,
                phone=contact_csv.phone,
                mobile_phone=contact_csv.mobile_phone,
                lat=contact_csv.lat,
                lon=contact_csv.lon,
            )
            referent = User.objects.filter(
                group=owning_group, email=contact_csv.referent_email
            ).first()
            if referent:
                contact_db.referents.add(referent)
            for tag in contact_csv.tags:
                contact_db.tags.add(tags[tag]["db_value"])
            contact["db_value"] = contact_db

            if not contact_csv.organization:
                continue

            linked_organization = Organization.objects.filter(
                owning_group=owning_group, name=contact_csv.organization
            )
            if linked_organization.count() > 1:
                # we have more than one organization matching the query,
                # we need to try to filter them out more
                linked_organization_try = linked_organization.filter(
                    town=contact_csv.town
                )
                if linked_organization_try.count() == 1:
                    linked_organization = linked_organization_try
            if linked_organization.count() != 1:
                raise AssertionError(
                    "Une et une seule organisation liée attendue mais nous en avons "
                    f"{linked_organization.count()} ; "
                    f"Contact : {contact_csv.first_name} {contact_csv.last_name} ; "
                    f"Structure : {contact_csv.organization}"
                )
            linked_organization = linked_organization.first()
            member_of_organizations[
                f"{contact_db.pk}->{linked_organization.pk}"
            ] = MemberOfOrganization.objects.create(
                owning_group=owning_group,
                contact=contact_db,
                organization=linked_organization,
                title_in_organization=contact_csv.title,
            )
        except Exception:
            raise Exception(f"CSV contact, ligne {contact_csv.line_nb}")


def _create_organizations(organizations, owning_group, tags):
    for organization in organizations.values():
        organization_csv = organization["csv_value"]
        try:
            organization_db = Organization.objects.create(
                owning_group=owning_group,
                name=organization_csv.name,
                reference=organization_csv.reference,
                type_of_organization=organization_csv.type_of_organization,
                address=organization_csv.address,
                zipcode=organization_csv.zipcode,
                town=organization_csv.town,
                country=organization_csv.country,
                email=organization_csv.email,
                website=organization_csv.website,
                phone=organization_csv.phone,
                lat=organization_csv.lat,
                lon=organization_csv.lon,
            )
            referent = User.objects.filter(
                group=owning_group, email=organization_csv.referent_email
            ).first()
            if referent:
                organization_db.referents.add(referent)
            for tag in organization_csv.tags:
                organization_db.tags.add(tags[tag]["db_value"])
            organization["db_value"] = organization_db
        except Exception:
            raise Exception(f"CSV structures, lignes {organization_csv.line_nb}")


@require_http_methods(["GET", "POST"])
def import_csv(request):
    if request.method == "GET":
        owning_groups = Group.objects.all().order_by("name")
        return render(request, "fac/admin/import_csv.html", context=locals())

    tags = {}
    organizations = {}
    contacts = {}
    member_of_organizations = {}
    duplicate_organizations = []
    duplicate_contacts = []
    already_existing_organizations = []
    already_existing_contacts = []
    already_existing_tags = []

    try:
        do_import_csv(
            request.FILES,
            int(request.POST["owning_group"]),
            organizations,
            contacts,
            tags,
            member_of_organizations,
            duplicate_organizations,
            duplicate_contacts,
            already_existing_organizations,
            already_existing_contacts,
            already_existing_tags,
        )
        added_organizations = [
            organization["db_value"]
            for organization in organizations.values()
            if "db_value" in organization
        ]
        added_contacts = [
            contact["db_value"]
            for contact in contacts.values()
            if "db_value" in contact
        ]
        added_tags = [tag["db_value"] for tag in tags.values() if "db_value" in tag]
        added_member_of_organizations = list(member_of_organizations.values())

        return render(request, "fac/admin/import_csv_done.html", context=locals())
    except Exception:
        logger.exception("Erreur lors de l'import")
        return render(
            request,
            "fac/admin/import_csv_error.html",
            context={"error": f"Erreur lors de l'import: {traceback.format_exc()}"},
        )

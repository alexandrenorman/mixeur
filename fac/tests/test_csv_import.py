import io

from django.test import TestCase, Client

from accounts.models import User
from accounts.tests import UserFactory, GroupFactory
from fac.admin.admin_views import cleanup_files, do_import_csv
from fac.models import Organization, Contact, Tag, MemberOfOrganization


class FakeFile:
    def __init__(self, content):
        self.fh = io.BytesIO(content.encode())

    def open(self):
        return self.fh


def noop(organizations, contacts):
    pass


class CSVImportTestCase(TestCase):
    def setUp(self):
        self.anonymous_client = Client()
        self.admin_client = Client()
        self.group = GroupFactory()
        admin = UserFactory(user_type="administrator", group=self.group, is_staff=True)
        self.referent = User.objects.create(
            group=self.group, email="referent@hespul.org"
        )
        from fac.admin import admin_views

        admin_views.add_lat_lon = noop
        assert self.admin_client.login(username=admin.email, password="password")

    def test_import_should_login(self):
        response = self.anonymous_client.get("/admin/fac/import_csv/")
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login", response.url)

    def test_import_get(self):
        response = self.admin_client.get("/admin/fac/import_csv/")
        self.assertEqual(response.status_code, 200)

    def test_import_clean(self):
        organizations_file = FakeFile(
            "Nom de la structure,Référent interne - merci de saisir une adresse email "
            "liée à un compte Mixeur existant,Référence interne (optionnel),"
            "Type de structure,Adresse,Code postal,Ville,Pays,Courriel (optionnel),"
            "Site (optionnel),Téléphone (format 0123456789) (optionnel),"
            "Tags (optionnels),Tag obligatoire,,\n"
            "Hespul,referent@hespul.org,,Banque,14 Place Jules Ferry,69006,Lyon,France"
            ",contact@hespul.org,"
            "😊"  # this should be removed by the cleaning process
            'http://hespul.org,0437478090,"photovoltaïque,sobriété",BAN-TEST,,,\n'
            ",,,,,,,,,,,,,\n"  # this should be removed by the cleaning process
            ",,,,,,,\n"  # this should be removed by the cleaning process
            "\n"  # this should be removed by the cleaning process
        )
        contacts_file = FakeFile(
            "Civilité,Prénom,Nom,Courriel,Adresse (optionnel),Code postal (optionnel),"
            "Ville (optionnel),Pays (optionnel) ,Téléphone (optionnel),"
            "Mobile (optionnel),Tags (optionnel),Structure associée,"
            "Titre/fonction dans la structure,Référent interne (optionnel) "
            "- merci de saisir une adresse email liée à un compte Mixeur existant\n"
            "M.,John,Smith,john.smith@hespul.org,,,,France,,,"
            "😊"  # this should be removed by the cleaning process
            "informatique,Hespul,Administrateur système,referent@hespul.org,,,\n"
            ",,,,,,,,,,,,,,,\n"  # this should be removed by the cleaning process
            ",,,,,,,\n"  # this should be removed by the cleaning process
            "\n"  # this should be removed by the cleaning process
        )
        organizations_file, contacts_file = cleanup_files(
            {"organizations": organizations_file, "contacts": contacts_file}
        )
        organizations_file_content = organizations_file.read()
        contacts_file_content = contacts_file.read()
        self.assertEquals(2, len(organizations_file_content.split("\n")))
        self.assertEquals(2, len(contacts_file_content.split("\n")))
        self.assertFalse("😊" in organizations_file_content)
        self.assertFalse("😊" in contacts_file_content)

    def test_do_import_csv(self):
        self.assertEquals(0, Organization.objects.count())
        self.assertEquals(0, Contact.objects.count())
        self.assertEquals(0, Tag.objects.count())
        self.assertEquals(0, MemberOfOrganization.objects.count())
        organizations_file = FakeFile(
            "Nom de la structure,Référent interne - merci de saisir une adresse email "
            "liée à un compte Mixeur existant,Référence interne (optionnel),"
            "Type de structure,Adresse,Code postal,Ville,Pays,Courriel (optionnel),"
            "Site (optionnel),Téléphone (format 0123456789) (optionnel),"
            "Tags (optionnels),Tag obligatoire\n"
            "Hespul,referent@hespul.org,12,Banque,14 Place Jules Ferry,69006,Lyon,"
            "France,contact@hespul.org,"
            'http://hespul.org,0437478090,"photovoltaïque,sobriété",BAN-TEST'
        )
        contacts_file = FakeFile(
            "Civilité,Prénom,Nom,Courriel,Adresse (optionnel),Code postal (optionnel),"
            "Ville (optionnel),Pays (optionnel) ,Téléphone (optionnel),"
            "Mobile (optionnel),Tags (optionnel),Structure associée,"
            "Titre/fonction dans la structure,Référent interne (optionnel) "
            "- merci de saisir une adresse email liée à un compte Mixeur existant\n"
            "M.,John,Smith,john.smith@hespul.org,14 Place Jules Ferry,69006,Lyon,France"
            ',0123456789,0623456789,"informatique,sobriété",Hespul,'
            "Administrateur système,referent@hespul.org"
        )
        do_import_csv(
            {"organizations": organizations_file, "contacts": contacts_file},
            self.group.pk,
            {},
            {},
            {},
            {},
            [],
            [],
            [],
            [],
            [],
        )
        self.assertEquals(1, Organization.objects.count())
        self.assertEquals(1, Contact.objects.count())
        self.assertEquals(4, Tag.objects.count())
        self.assertEquals(1, MemberOfOrganization.objects.count())
        organization = Organization.objects.first()
        self.assertEquals("Hespul", organization.name)
        self.assertEquals("12", organization.reference)
        self.assertEquals("Banque", organization.type_of_organization)
        self.assertEquals("14 Place Jules Ferry", organization.address)
        self.assertEquals("69006", organization.zipcode)
        self.assertEquals("Lyon", organization.town)
        self.assertEquals("France", organization.country)
        self.assertEquals("contact@hespul.org", organization.email)
        self.assertEquals("http://hespul.org", organization.website)
        self.assertEquals("0437478090", organization.phone_cache)
        self.assertEquals(self.referent.pk, organization.referents.first().pk)
        self.assertEquals(
            {"photovoltaïque", "sobriété", "BAN-TEST"},
            {tag.name for tag in organization.tags.all()},
        )
        contact = Contact.objects.first()
        self.assertEquals("M.", contact.civility)
        self.assertEquals("John", contact.first_name)
        self.assertEquals("Smith", contact.last_name)
        self.assertEquals("john.smith@hespul.org", contact.email)
        self.assertEquals("14 Place Jules Ferry", contact.address)
        self.assertEquals("69006", contact.zipcode)
        self.assertEquals("Lyon", contact.town)
        self.assertEquals("France", contact.country)
        self.assertEquals("0123456789", contact.phone_cache)
        self.assertEquals("0623456789", contact.mobile_phone_cache)
        self.assertEquals(
            {"informatique", "sobriété"}, {tag.name for tag in contact.tags.all()}
        )
        self.assertEquals(
            "Hespul", contact.memberoforganization_set.first().organization.name
        )
        self.assertEquals(
            "Administrateur système",
            contact.memberoforganization_set.first().title_in_organization,
        )
        self.assertEquals(self.referent.pk, contact.referents.first().pk)

    def test_import_post(self):
        self.assertEquals(0, Organization.objects.count())
        self.assertEquals(0, Contact.objects.count())
        self.assertEquals(0, Tag.objects.count())
        self.assertEquals(0, MemberOfOrganization.objects.count())
        organizations_file = io.StringIO(
            "Nom de la structure,Référent interne - merci de saisir une adresse email "
            "liée à un compte Mixeur existant,Référence interne (optionnel),"
            "Type de structure,Adresse,Code postal,Ville,Pays,Courriel (optionnel),"
            "Site (optionnel),Téléphone (format 0123456789) (optionnel),"
            "Tags (optionnels),Tag obligatoire,,\n"
            "Hespul,referent@hespul.org,,Banque,14 Place Jules Ferry,69006,Lyon,France"
            ",contact@hespul.org,"
            "😊"  # this should be removed by the cleaning process
            'http://hespul.org,0437478090,"photovoltaïque,sobriété",BAN-TEST,,,\n'
            "Alec,,,,,,,,,,,,,\n"
            ",,,,,,,,,,,,,\n"  # this should be removed by the cleaning process
            ",,,,,,,\n"  # this should be removed by the cleaning process
            "\n"  # this should be removed by the cleaning process
        )
        contacts_file = io.StringIO(
            "Civilité,Prénom,Nom,Courriel,Adresse (optionnel),Code postal (optionnel),"
            "Ville (optionnel),Pays (optionnel) ,Téléphone (optionnel),"
            "Mobile (optionnel),Tags (optionnel),Structure associée,"
            "Titre/fonction dans la structure,Référent interne (optionnel) "
            "- merci de saisir une adresse email liée à un compte Mixeur existant\n"
            "M.,John,Smith,john.smith@hespul.org,,,,France,,,"
            "😊"  # this should be removed by the cleaning process
            "informatique,Hespul,Administrateur système,referent@hespul.org,,,\n"
            "Mme,Marie,Martin,,,,,,,,,,,,,,\n"
            ",,,,,,,,,,,,,,,\n"  # this should be removed by the cleaning process
            ",,,,,,,\n"  # this should be removed by the cleaning process
            "\n"  # this should be removed by the cleaning process
        )
        response = self.admin_client.post(
            "/admin/fac/import_csv/",
            data={
                "organizations": organizations_file,
                "contacts": contacts_file,
                "owning_group": self.group.pk,
            },
        )
        self.assertEqual(response.status_code, 200)

        self.assertEquals(2, Organization.objects.count())
        self.assertEquals(2, Contact.objects.count())
        self.assertEquals(4, Tag.objects.count())
        self.assertEquals(1, MemberOfOrganization.objects.count())
        organization = Organization.objects.filter(name="Hespul").first()
        self.assertEquals("Hespul", organization.name)
        self.assertEquals("Banque", organization.type_of_organization)
        self.assertEquals("14 Place Jules Ferry", organization.address)
        self.assertEquals("69006", organization.zipcode)
        self.assertEquals("Lyon", organization.town)
        self.assertEquals("France", organization.country)
        self.assertEquals("contact@hespul.org", organization.email)
        self.assertEquals("http://hespul.org", organization.website)
        self.assertEquals("0437478090", organization.phone_cache)
        self.assertEquals(
            {"photovoltaïque", "sobriété", "BAN-TEST"},
            {tag.name for tag in organization.tags.all()},
        )
        self.assertEquals(self.referent.pk, organization.referents.first().pk)
        contact = Contact.objects.filter(first_name="John").first()
        self.assertEquals("M.", contact.civility)
        self.assertEquals("John", contact.first_name)
        self.assertEquals("Smith", contact.last_name)
        self.assertEquals("john.smith@hespul.org", contact.email)
        self.assertEquals("France", contact.country)
        self.assertEquals({"informatique"}, {tag.name for tag in contact.tags.all()})
        self.assertEquals(
            "Hespul", contact.memberoforganization_set.first().organization.name
        )
        self.assertEquals(
            "Administrateur système",
            contact.memberoforganization_set.first().title_in_organization,
        )
        self.assertEquals(self.referent.pk, contact.referents.first().pk)

"""
Ce script permet de lancer la vérification de l'ensemble des Contacts / Structures

Pour le lancer :

    inv run -c "check_incomplete_data"
"""

from django.core.management.base import BaseCommand

from fac.models import (
    Contact,
    IncompleteModel,
    Organization,
)


class Command(BaseCommand):
    help = "Verify incomplete data for Contacts / Organizations"  # NOQA: A003

    def handle(self, *args, **options):
        print("Checking Contacts")
        for contact in Contact.objects.all():
            result = IncompleteModel.check_incomplete_model_and_save(contact)
            if result:
                print(
                    f" - invalid contact {contact.pk} - {contact.full_name} / {contact.email}"
                )

        print("Checking Organizations")
        for organization in Organization.objects.all():
            result = IncompleteModel.check_incomplete_model_and_save(organization)
            if result:
                print(
                    f" - invalid organization {organization.pk} - {organization.name}"
                )

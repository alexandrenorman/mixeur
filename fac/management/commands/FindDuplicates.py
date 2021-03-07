from django.core.management.base import BaseCommand

from fac.models.contacts_duplicate import find_duplicated_contacts, ContactsDuplicate


class Command(BaseCommand):
    help = "Find duplicated contacts."

    def handle(self, *args, **options):
        duplicates = find_duplicated_contacts()

        for k in duplicates:
            existing = ContactsDuplicate.objects.all()
            for contact in duplicates[k]:
                existing = existing.filter(contacts=contact)

            if existing:
                continue

            cd = ContactsDuplicate()
            cd.save()
            for contact in duplicates[k]:
                cd.contacts.add(contact)

            cd.save()

        return

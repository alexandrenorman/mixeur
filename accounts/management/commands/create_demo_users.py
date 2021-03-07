# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError

from accounts.models import User, Group


class Command(BaseCommand):
    """
    """

    help = "Create demo users"

    def handle(self, *args, **options):
        admin_group, _ = Group.objects.get_or_create(
            name="Structure Admin", is_admin=True
        )
        group, _ = Group.objects.get_or_create(name="Structure Test")
        data = [
            {
                "method": User.objects.create_client,
                "email": "client@test.org",
                "password": "client_test",
                "first_name": "Gérard",
                "last_name": "Majax",
            },
            {
                "method": User.objects.create_advisor,
                "email": "conseiller@test.org",
                "password": "conseiller_test",
                "first_name": "Jean-Pierre",
                "last_name": "Vallarino",
                "group": group,
            },
            {
                "method": User.objects.create_manager,
                "email": "manager@test.org",
                "password": "manager_test",
                "first_name": "Pierre",
                "last_name": "Edernac",
                "group": admin_group,
            },
            {
                "method": User.objects.create_administrator,
                "email": "admin@test.org",
                "password": "admin_test",
                "first_name": "Gandalf",
                "last_name": "Le Blanc",
                "group": None,
            },
        ]
        for item in data:
            try:
                user = item["method"](
                    email=item["email"],
                    password=item["password"],
                    first_name=item["first_name"],
                    last_name=item["last_name"],
                )
            except IntegrityError:
                self.stdout.write(f"User already created {item['email']}")
            else:
                self.stdout.write(f"User created {item['email']}")
                if "group" in item:
                    user.group = item["group"]
                    user.save()

        return

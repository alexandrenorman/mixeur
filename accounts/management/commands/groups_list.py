# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from django.db.models import Count

from accounts.models import Group


class Command(BaseCommand):
    """"""

    help = "Show groups list"  # NOQA: A003

    def handle(self, *args, **options):
        for group in (
            Group.objects.filter(is_active=True)
            .order_by("name")
            .annotate(nb_users=Count("profile"))
            .all()
            .values("pk", "name", "nb_users")
        ):
            print(f"{group['pk']}\t{group['name']} ({group['nb_users']} utilisateurs)")

        return

"""
Ce script permet de générer tous les modèles de dossiers, actions, etc, pour
Actimmo.

Pour le lancer :

    inv run -c "populate_actimmo"

S'il rencontre un problème à l'exécution, rien ne sera créé.

Pour supprimer tout ce qui a été créé : supprimer le projet Actimmo, ainsi que
les trois types de valorisation.
"""
from django.core.management.base import BaseCommand

from accounts.models import Group


class Command(BaseCommand):
    help = "Count users by group"  # NOQA: A003

    def handle(self, *args, **options):
        out = ""
        for g in Group.objects.all():
            users = [u.email for u in g.users if u.is_active]
            out += f"\n* Groupe {g.name} => {len(users)} utilisateurs"

        print(out)

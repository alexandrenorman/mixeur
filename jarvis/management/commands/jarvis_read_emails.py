from django.core.management.base import BaseCommand

from jarvis.jarvis import Jarvis


class Command(BaseCommand):
    help = "Jarvis, read your mailbox."  # NOQA: A003

    def handle(self, *args, **options):  # NOQA: C901
        jarvis = Jarvis()
        jarvis.read_mails()
        return

from django.core.management.base import BaseCommand
from white_labelling.helpers import generate_traefik_configuration


class Command(BaseCommand):
    """
    """

    help = "Re-generate traefik configuration (traefik/conf/configuration.yaml)"

    def handle(self, *args, **options):

        # self.stdout.write(f"WhiteLabelling [{white_labelling.domain}] crée")
        generate_traefik_configuration()

# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from white_labelling.models import WhiteLabelling


class Command(BaseCommand):
    """
    """

    help = "Create base WhiteLabelling for mixeur.docker.local"

    def handle(self, *args, **options):

        white_labelling, _ = WhiteLabelling.objects.get_or_create(
            domain="mixeur.docker.local"
        )

        white_labelling.domain = "mixeur.docker.local"
        white_labelling.site_title = "mixeur.docker.local"
        white_labelling.header = '<div class="header">\n<h1>Dialogwatt</h1>\n</div>'
        white_labelling.footer = '<div class="footer">\n<h4>Développement en cours (branche dev)</h4>\n</div>'
        white_labelling.css = (
            ".header {\n  text-align: center;\n  height: 100px;\n"
            "  background-color: #3986c2;\n}\n\n.header h1 {\n  color: #fff;\n}\n"
        )
        white_labelling.is_default = True

        white_labelling.save()
        self.stdout.write(f"WhiteLabelling [{white_labelling.domain}] crée")

        return

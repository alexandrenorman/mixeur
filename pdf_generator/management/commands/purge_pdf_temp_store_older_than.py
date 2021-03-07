# -*- coding: utf-8 -*-
from django.utils import timezone
from datetime import timedelta
from django.core.management.base import BaseCommand

from pdf_generator.models import PdfTempStore


class Command(BaseCommand):
    help = "Delete objects older than 1 day"

    def add_arguments(self, parser):
        parser.add_argument(
            "hours",
            type=int,
            help="Indicates after how many hours we purge the PdfTempStore",
        )

    def handle(self, *args, **kwargs):
        hours = kwargs["hours"]
        PdfTempStore.objects.filter(
            created_at__lt=timezone.now() - timedelta(hours=hours)
        ).delete()
        self.stdout.write(f"Deleted objects older than {hours} hours")
        return

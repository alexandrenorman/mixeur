# Generated by Django 2.1.8 on 2019-04-09 08:17

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.utils.timezone
import core.models
import helpers.mixins.universal_repr_mixin
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PdfTempStore',
            fields=[
                ('created_at', models.DateField(default=django.utils.timezone.now, editable=False)),
                ('updated_at', core.models.AutoDateTimeField(default=django.utils.timezone.now, editable=False)),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('data', django.contrib.postgres.fields.jsonb.JSONField()),
            ],
            options={
                'verbose_name': 'Pdf Temp',
            },
            bases=(helpers.mixins.universal_repr_mixin.UniversalReprMixin, models.Model),
        ),
    ]

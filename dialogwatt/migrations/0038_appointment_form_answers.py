# Generated by Django 2.2.10 on 2020-05-27 15:00

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dialogwatt', '0037_appointment_history'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='form_answers',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
    ]

# Generated by Django 2.2.10 on 2020-08-10 12:50

import core.models
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('listepro', '0013_auto_20200716_1420'),
    ]

    operations = [
        migrations.CreateModel(
            name='Helper',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('updated_at', core.models.AutoDateTimeField(default=django.utils.timezone.now, editable=False)),
                ('order', models.IntegerField(default=0, verbose_name="Ordre d'affichage")),
                ('name', models.CharField(max_length=128)),
                ('help_text', models.TextField(blank=True, null=True, verbose_name="Texte de l'aide")),
            ],
            options={
                'verbose_name': 'Aide',
                'verbose_name_plural': 'Aides',
            },
        ),
    ]

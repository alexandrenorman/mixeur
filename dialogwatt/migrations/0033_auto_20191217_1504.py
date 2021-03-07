# Generated by Django 2.2.8 on 2019-12-17 14:04

import dialogwatt.models.place
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dialogwatt', '0032_auto_20191007_1716'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='appointment',
            options={'ordering': ('start_date',), 'verbose_name': 'Rendez-vous', 'verbose_name_plural': 'Rendez-vous'},
        ),
        migrations.AlterModelOptions(
            name='reason',
            options={'ordering': ('name',), 'verbose_name': 'Motif de rendez-vous', 'verbose_name_plural': 'Motifs de rendez-vous'},
        ),
        migrations.AlterModelOptions(
            name='slot',
            options={'ordering': ('start_date',), 'verbose_name': 'Créneau', 'verbose_name_plural': 'Créneaux'},
        ),
        migrations.AddField(
            model_name='place',
            name='img',
            field=models.ImageField(blank=True, null=True, upload_to=dialogwatt.models.place.places_directory_path),
        ),
        migrations.AlterField(
            model_name='place',
            name='lon',
            field=models.DecimalField(decimal_places=6, default=0, max_digits=9, verbose_name='Longitude'),
        ),
    ]

# Generated by Django 2.2.11 on 2020-03-31 09:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('white_labelling', '0017_auto_20200318_1740'),
    ]

    operations = [
        migrations.AddField(
            model_name='whitelabelling',
            name='actimmo_map_remove_margins',
            field=models.BooleanField(default=False, verbose_name='Supprimer les marges sur la cartographie (pour iframe)'),
        ),
    ]

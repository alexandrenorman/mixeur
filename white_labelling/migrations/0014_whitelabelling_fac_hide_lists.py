# Generated by Django 2.2.9 on 2020-02-07 13:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('white_labelling', '0013_auto_20200212_0946'),
    ]

    operations = [
        migrations.AddField(
            model_name='whitelabelling',
            name='fac_hide_lists',
            field=models.BooleanField(default=True, verbose_name='Cacher les listes'),
        ),
    ]

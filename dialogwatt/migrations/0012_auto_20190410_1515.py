# Generated by Django 2.2 on 2019-04-10 13:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dialogwatt', '0011_auto_20190409_1635'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='all_places',
            field=models.BooleanField(default=True, verbose_name='Tous lieux ?'),
        ),
        migrations.AddField(
            model_name='notification',
            name='all_reasons',
            field=models.BooleanField(default=True, verbose_name='Tous motifs ?'),
        ),
    ]

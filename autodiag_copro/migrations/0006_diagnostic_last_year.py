# Generated by Django 2.1.5 on 2019-04-01 12:59

import autodiag_copro.models.diagnostic
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autodiag_copro', '0005_auto_20190325_0942'),
    ]

    operations = [
        migrations.AddField(
            model_name='diagnostic',
            name='last_year',
            field=models.PositiveSmallIntegerField(default=2019, validators=[autodiag_copro.models.diagnostic.validation_absolute_positive], verbose_name='Dernière année évaluée'),
            preserve_default=False,
        ),
    ]

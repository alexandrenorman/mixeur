# Generated by Django 2.2.10 on 2020-12-01 13:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('white_labelling', '0036_auto_20201201_1213'),
    ]

    operations = [
        migrations.AlterField(
            model_name='whitelabelling',
            name='listepro_is_active',
            field=models.BooleanField(default=False, verbose_name='Activer la listepro'),
        ),
    ]
# Generated by Django 2.2.10 on 2020-09-07 10:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('white_labelling', '0027_whitelabelling_preco_immo_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='whitelabelling',
            name='enable_django_admin',
            field=models.BooleanField(default=False, verbose_name='Accès admin django'),
        ),
    ]
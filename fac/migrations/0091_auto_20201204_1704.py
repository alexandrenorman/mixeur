# Generated by Django 2.2.17 on 2020-12-04 16:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fac', '0090_remove_null'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='address',
            field=models.CharField(blank=True, max_length=255, verbose_name='Adresse'),
        ),
        migrations.AlterField(
            model_name='organization',
            name='country',
            field=models.CharField(blank=True, max_length=100, verbose_name='Pays'),
        ),
        migrations.AlterField(
            model_name='organization',
            name='description',
            field=models.TextField(blank=True, max_length=20000, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='organization',
            name='fax_cache',
            field=models.CharField(blank=True, max_length=100, verbose_name='Cache pour le numéro de fax'),
        ),
        migrations.AlterField(
            model_name='organization',
            name='phone_cache',
            field=models.CharField(blank=True, max_length=100, verbose_name='Cache pour le numéro de téléphone'),
        ),
        migrations.AlterField(
            model_name='organization',
            name='town',
            field=models.CharField(blank=True, max_length=255, verbose_name='Ville'),
        ),
        migrations.AlterField(
            model_name='organization',
            name='zipcode',
            field=models.CharField(blank=True, max_length=50, verbose_name='Code postal'),
        ),
    ]
# Generated by Django 2.2.6 on 2019-11-21 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fac', '0023_organization_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='civility',
            field=models.CharField(choices=[('-', 'Non précisé'), ('M.', 'M.'), ('Mme', 'Mme')], default='-', max_length=10, verbose_name='Civilité'),
        ),
    ]
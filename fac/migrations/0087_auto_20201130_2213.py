# Generated by Django 2.2.17 on 2020-11-30 21:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fac', '0086_auto_20201126_1053'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='civility',
            field=models.CharField(choices=[('-', 'Non précisé'), ('M.', 'M.'), ('Mme', 'Mme')], default='O', max_length=10, verbose_name='Civilité'),
        ),
    ]

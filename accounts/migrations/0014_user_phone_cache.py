# Generated by Django 2.2 on 2019-05-22 07:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0013_group_phone'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='phone_cache',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Cache pour le numéro de téléphone'),
        ),
    ]

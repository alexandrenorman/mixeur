# Generated by Django 2.2.3 on 2019-10-21 08:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fac', '0016_create_trigram_extension'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contact',
            old_name='phone_mobile',
            new_name='mobile_phone',
        ),
        migrations.RenameField(
            model_name='contact',
            old_name='phone_mobile_cache',
            new_name='mobile_phone_cache',
        ),
    ]

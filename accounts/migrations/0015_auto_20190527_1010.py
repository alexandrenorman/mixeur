# Generated by Django 2.2 on 2019-05-27 08:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0014_user_phone_cache'),
    ]

    operations = [
        migrations.RenameField(
            model_name='rgpdconsent',
            old_name='allow_to_share_my_information_with_ADEME',
            new_name='allow_to_share_my_information_with_ademe',
        ),
    ]

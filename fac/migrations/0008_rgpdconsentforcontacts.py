# Generated by Django 2.2.2 on 2019-06-09 14:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fac', '0007_auto_20190609_0006'),
    ]

    operations = [
        migrations.CreateModel(
            name='RgpdConsentForContacts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_date', models.DateTimeField(auto_now_add=True, verbose_name='Date de création')),
                ('allow_to_keep_data', models.BooleanField(default=True, verbose_name='Permettre la conservation de mes données dans le système de traitement.')),
                ('allow_to_use_email_to_send_reminder', models.BooleanField(default=True, verbose_name="Permettre l'utilisation de mon email pour envoyer un rappel de rendez-vous ou des informations liées à mon dossier.")),
                ('allow_to_use_phone_number_to_send_reminder', models.BooleanField(default=True, verbose_name="Permettre l'utilisation de mon numéro de téléphone pour envoyer un rappel de rendez-vous.")),
                ('allow_to_share_my_information_with_my_advisor', models.BooleanField(default=True, verbose_name="Permettre le partage de mes informations avec l'EIE qui suit mon dossier.")),
                ('allow_to_share_my_information_with_ademe', models.BooleanField(default=True, verbose_name="Permettre le partage de mes informations avec l'ademe à des fins statistiques.")),
                ('contact', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fac.Contact')),
            ],
            options={
                'verbose_name': 'RgpdConsent',
                'verbose_name_plural': 'RgpdConsents',
                'ordering': ['-creation_date'],
            },
        ),
    ]

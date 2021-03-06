# Generated by Django 2.1.3 on 2018-11-21 15:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('white_labelling', '0001_initial'),
        ('accounts', '0004_remove_user_username'),
    ]

    operations = [
        migrations.CreateModel(
            name='RgpdConsent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_date', models.DateTimeField(auto_now_add=True, verbose_name='Date de création')),
                ('allow_to_keep_data', models.BooleanField(default=True, verbose_name='Permettre la conservation de mes données dans le système de traitement.')),
                ('allow_to_use_email_to_send_reminder', models.BooleanField(default=True, verbose_name="Permettre l'utilisation de mon email pour envoyer un rappel de rendez-vous ou des informations liées à mon dossier.")),
                ('allow_to_use_phone_number_to_send_reminder', models.BooleanField(default=True, verbose_name="Permettre l'utilisation de mon numéro de téléphone pour envoyer un rappel de rendez-vous.")),
                ('allow_to_share_my_information_with_my_advisor', models.BooleanField(default=True, verbose_name="Permettre le partage de mes informations avec l'EIE qui suit mon dossier.")),
                ('allow_to_share_my_information_with_ADEME', models.BooleanField(default=True, verbose_name="Permettre le partage de mes informations avec l'ADEME à des fins statistiques.")),
            ],
            options={
                'verbose_name': 'RgpdConsent',
                'verbose_name_plural': 'RgpdConsents',
                'ordering': ['-creation_date'],
            },
        ),
        migrations.RemoveField(
            model_name='group',
            name='domainname',
        ),
        migrations.RemoveField(
            model_name='group',
            name='perm',
        ),
        migrations.RemoveField(
            model_name='group',
            name='user',
        ),
        migrations.RemoveField(
            model_name='user',
            name='primary_group',
        ),
        migrations.AddField(
            model_name='user',
            name='address',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Adresse'),
        ),
        migrations.AddField(
            model_name='user',
            name='group',
            field=models.ForeignKey(blank=True, help_text="Structure d'appartenance", null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='profile', to='accounts.Group', verbose_name='Groupe'),
        ),
        migrations.AddField(
            model_name='user',
            name='phone',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=100, null=True, verbose_name='Numéro de téléphone'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_type',
            field=models.CharField(choices=[('client', 'Client'), ('advisor', 'Conseiller'), ('manager', 'Responsable'), ('administrator', 'Administrateur')], default='client', max_length=20, verbose_name="Profil d'utilisateur"),
        ),
        migrations.AddField(
            model_name='user',
            name='white_labelling',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='profile', to='white_labelling.WhiteLabelling', verbose_name='Domaine / marque blanche'),
        ),
        migrations.AddField(
            model_name='rgpdconsent',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]

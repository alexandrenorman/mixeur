# Generated by Django 2.2.2 on 2019-06-04 12:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dialogwatt', '0018_appointment_subject'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='trigger',
            field=models.CharField(choices=[('created_account', "Création d'un compte par le contact"), ('created_client', "Création d'un rdv par le contact"), ('changed_client', "Modification d'un rdv par le contact"), ('canceled_client', "Annulation d'un rdv par le contact"), ('created_advisor', "Création d'un rdv par le conseiller"), ('changed_advisor', "Modification d'un rdv par le conseiller"), ('canceled_advisor', "Annulation d'un rdv par le conseiller")], max_length=100, verbose_name='Déclencheur'),
        ),
    ]

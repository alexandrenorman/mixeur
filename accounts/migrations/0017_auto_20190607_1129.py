# Generated by Django 2.2 on 2019-06-07 09:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0016_auto_20190527_1015'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_type',
            field=models.CharField(choices=[('contact', 'Contact'), ('client', 'Client'), ('advisor', 'Conseiller'), ('manager', 'Responsable'), ('administrator', 'Administrateur')], default='client', max_length=20, verbose_name="Profil d'utilisateur"),
        ),
    ]

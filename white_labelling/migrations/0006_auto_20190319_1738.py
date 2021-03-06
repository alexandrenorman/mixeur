# Generated by Django 2.1.7 on 2019-03-19 16:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('white_labelling', '0005_auto_20181210_1818'),
    ]

    operations = [
        migrations.AddField(
            model_name='whitelabelling',
            name='autodiag_name',
            field=models.CharField(default='AutodiagCopro', max_length=100, verbose_name="Nom de l'application Autodiag"),
        ),
        migrations.AddField(
            model_name='whitelabelling',
            name='dialogwatt_name',
            field=models.CharField(default='DialogWatt', max_length=100, verbose_name="Nom de l'application DialogWatt"),
        ),
        migrations.AddField(
            model_name='whitelabelling',
            name='visit_report_name',
            field=models.CharField(default='Rapport de visite', max_length=100, verbose_name="Nom de l'application Rapport de visite"),
        ),
    ]

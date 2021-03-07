# Generated by Django 2.2.9 on 2020-02-12 08:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('white_labelling', '0012_whitelabelling_smtp_account'),
    ]

    operations = [
        migrations.AddField(
            model_name='whitelabelling',
            name='old_thermix_baseline',
            field=models.CharField(default='Comparer les systèmes de production de chauffage', max_length=100, verbose_name="Baseline de l'application Thermix (iframe)"),
        ),
        migrations.AddField(
            model_name='whitelabelling',
            name='old_thermix_is_active',
            field=models.BooleanField(default=True, verbose_name="Activer l'ancien Thermix en iframe"),
        ),
        migrations.AddField(
            model_name='whitelabelling',
            name='old_thermix_name',
            field=models.CharField(default='Thermix', max_length=100, verbose_name="Nom de l'application Thermix (iframe)"),
        ),
        migrations.AlterField(
            model_name='whitelabelling',
            name='thermix_is_active',
            field=models.BooleanField(default=False, verbose_name='Activer Thermix'),
        ),
    ]
# Generated by Django 2.2.10 on 2020-11-19 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fac', '0083_auto_20201027_1517'),
        ('custom_forms', '0004_auto_20201117_1045'),
    ]

    operations = [
        migrations.AddField(
            model_name='customform',
            name='action_models',
            field=models.ManyToManyField(blank=True, related_name='custom_forms', to='fac.ActionModel', verbose_name="Modèle d'action"),
        ),
    ]
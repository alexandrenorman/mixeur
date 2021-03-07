# Generated by Django 2.2.3 on 2019-07-31 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('visit_report', '0013_auto_20190726_1237'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workrecommendation',
            name='nature',
            field=models.CharField(choices=[('roof-insulation', 'Isolation de la toiture'), ('wall-insulation', 'Isolation des murs'), ('floor-insulation', 'Isolation du plancher bas'), ('carpentry-replacement', 'Remplacement des menuiseries'), ('ventilation', 'VMC'), ('heating-production', 'Production de chaleur'), ('heating-emitter', 'Production de chaleur'), ('hot-water-production', "Production d'eau chaude sanitaire"), ('heating-control', 'Régulation du système de chauffage'), ('photovoltaic', 'Installation de panneaux solaires photovoltaïques'), ('eco-gestures', 'Eco gestes'), ('calorifuge', 'Calorifuge'), ('water-tank-insulation', 'water-tank-insulation'), ('additional-costs', 'Frais supplémentaires')], max_length=50, verbose_name='Type'),
        ),
    ]
# Generated by Django 2.1.5 on 2019-03-25 08:42

import autodiag_copro.models.copro
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autodiag_copro', '0004_auto_20190321_1505'),
    ]

    operations = [
        migrations.AlterField(
            model_name='copro',
            name='heating_individualisation_costs',
            field=models.DecimalField(decimal_places=2, max_digits=20, null=True, validators=[autodiag_copro.models.copro.validation_absolute_positive], verbose_name="Frais d'individualisation"),
        ),
        migrations.AlterField(
            model_name='copro',
            name='heating_maintenance_contract_P2_P3_cost',
            field=models.DecimalField(decimal_places=2, max_digits=20, null=True, validators=[autodiag_copro.models.copro.validation_absolute_positive], verbose_name='Montant du contrat de maintenance P2 + P3'),
        ),
        migrations.AlterField(
            model_name='copro',
            name='heating_maintenance_contract_P2_cost',
            field=models.DecimalField(decimal_places=2, max_digits=20, null=True, validators=[autodiag_copro.models.copro.validation_absolute_positive], verbose_name='Montant du contrat de maintenance P2'),
        ),
    ]

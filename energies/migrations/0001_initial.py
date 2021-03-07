# Generated by Django 2.1.5 on 2019-03-17 17:22

import core.models
import django.db.models.deletion
import django.utils.timezone
import energies.models.energy
from django.db import migrations, models


def validation_absolute_positive():
    pass


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Energy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateField(default=django.utils.timezone.now, editable=False)),
                ('updated_at', core.models.AutoDateTimeField(default=django.utils.timezone.now, editable=False)),
                ('identifier', models.CharField(max_length=30, verbose_name="Identifiant d'énergie")),
                ('primary_energy_ratio', models.DecimalField(decimal_places=10, max_digits=20, validators=[validation_absolute_positive], verbose_name="Ratio d'énergie primaire")),
                ('ghg_ratio', models.DecimalField(decimal_places=10, max_digits=20, validators=[validation_absolute_positive], verbose_name='Ratio gaz à effet de serre')),
                ('carbon_tax', models.BooleanField(default=False, verbose_name='Assujeti à la taxe carbone ?')),
                ('pci_ratio', models.PositiveSmallIntegerField(null=True, validators=[validation_absolute_positive], verbose_name='Ratio de pouvoir calorifique inférieur')),
                ('density_ratio', models.DecimalField(decimal_places=10, max_digits=20, null=True, validators=[validation_absolute_positive], verbose_name='Ratio de densité')),
            ],
            options={
                'verbose_name': 'Énergie',
            },
        ),
        migrations.CreateModel(
            name='YearlyEnergyPrice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateField(default=django.utils.timezone.now, editable=False)),
                ('updated_at', core.models.AutoDateTimeField(default=django.utils.timezone.now, editable=False)),
                ('year', models.PositiveSmallIntegerField(verbose_name='Année')),
                ('price', models.DecimalField(decimal_places=2, max_digits=20, null=True, validators=[validation_absolute_positive], verbose_name='Prix')),
                ('energy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='yearly_energy_price', to='energies.Energy', verbose_name='Énergie')),
            ],
            options={
                'verbose_name': 'Prix des énergies par année',
            },
        ),
        migrations.AlterUniqueTogether(
            name='yearlyenergyprice',
            unique_together={('year', 'energy')},
        ),
    ]
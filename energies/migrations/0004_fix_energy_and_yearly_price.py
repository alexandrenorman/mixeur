from django.db import migrations, models
from decimal import Decimal
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('energies', '0003_auto_20190430_1356'),
    ]

    operations = [
        migrations.AlterField(
            model_name='energy',
            name='identifier',
            field=models.CharField(choices=[('oil', 'Fioul'), ('gaz_b0', 'Gaz B0'), ('gaz_b1', 'Gaz B1'), ('propane', 'Propane'), ('electricity', 'Électricité'), ('wood', 'Bois'), ('shredded_wood', 'Bois déchiqueté'), ('bulk_granules', 'Bois granulés en vrac'), ('bag_granules', 'Bois granulés en sac'), ('network', 'Réseau')], max_length=30, unique=True, verbose_name="Identifiant d'énergie"),
        ),
        migrations.AlterField(
            model_name='energy',
            name='density_ratio',
            field=models.DecimalField(decimal_places=10, max_digits=20, null=True, validators=[django.core.validators.MinValueValidator(Decimal('1'))], verbose_name='Ratio de densité'),
        ),
        migrations.AlterField(
            model_name='energy',
            name='ghg_ratio',
            field=models.DecimalField(decimal_places=10, max_digits=20, validators=[django.core.validators.MinValueValidator(Decimal('1'))], verbose_name='Ratio gaz à effet de serre'),
        ),
        migrations.AlterField(
            model_name='energy',
            name='pci_ratio',
            field=models.PositiveSmallIntegerField(null=True, validators=[django.core.validators.MinValueValidator(Decimal('1'))], verbose_name='Ratio de pouvoir calorifique inférieur'),
        ),
        migrations.AlterField(
            model_name='energy',
            name='primary_energy_ratio',
            field=models.DecimalField(decimal_places=10, max_digits=20, validators=[django.core.validators.MinValueValidator(Decimal('1'))], verbose_name="Ratio d'énergie primaire"),
        ),

        migrations.AlterField(
            model_name='yearlyenergyprice',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=20, null=True, validators=[django.core.validators.MinValueValidator(Decimal('1'))], verbose_name='Prix'),
        ),
    ]

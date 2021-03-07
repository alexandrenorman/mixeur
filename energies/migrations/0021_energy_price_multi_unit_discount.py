# Generated by Django 2.2.3 on 2019-07-19 08:40

from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('energies', '0020_energy_price_variation_data'),
    ]

    operations = [
        migrations.AddField(
            model_name='energy',
            name='price_multi_unit_discount',
            field=models.DecimalField(decimal_places=2, default=Decimal('0.85'), max_digits=3, verbose_name='Ratio appliqué sur le prix pour logement collectifs'),
        ),
    ]
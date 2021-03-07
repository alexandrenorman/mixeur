# Generated by Django 2.2.3 on 2019-07-05 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('energies', '0018_secondaryefficiency_data'),
    ]

    operations = [
        migrations.AddField(
            model_name='energy',
            name='price_variation',
            field=models.DecimalField(decimal_places=5, default=0, max_digits=6, verbose_name='Variation du prix depuis 2002'),
            preserve_default=False,
        ),
    ]

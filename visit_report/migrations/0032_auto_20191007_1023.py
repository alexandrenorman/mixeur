# Generated by Django 2.2.3 on 2019-10-07 08:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('visit_report', '0031_auto_20191003_1641'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='is_secondary_scenario_displayed',
            field=models.BooleanField(default=True, verbose_name='Afficher le scénario secondaire'),
        ),
        migrations.AlterField(
            model_name='scenario',
            name='label',
            field=models.CharField(max_length=50, verbose_name='Label'),
        ),
    ]
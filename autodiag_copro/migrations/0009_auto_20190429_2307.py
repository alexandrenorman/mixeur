# Generated by Django 2.2 on 2019-04-29 21:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autodiag_copro', '0008_auto_20190423_2123'),
    ]

    operations = [
        migrations.AlterField(
            model_name='copro',
            name='ref_dju_correction',
            field=models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Correction DJU de référence'),
        ),
    ]
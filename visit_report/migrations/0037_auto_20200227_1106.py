# Generated by Django 2.2.10 on 2020-02-27 10:06

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('visit_report', '0036_auto_20200221_2119'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='visit_date',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='Date de la visite'),
        ),
    ]

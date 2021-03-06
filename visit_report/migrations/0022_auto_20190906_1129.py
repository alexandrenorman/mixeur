# Generated by Django 2.2.3 on 2019-09-06 09:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('visit_report', '0021_report_visit_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='financialaid',
            name='nature',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Type'),
        ),
        migrations.AddField(
            model_name='financing',
            name='nature',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Type'),
        ),
        migrations.AddField(
            model_name='scenariosummary',
            name='nature',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Type'),
        ),
        migrations.AddField(
            model_name='scenariosummary',
            name='selected',
            field=models.BooleanField(default=False, verbose_name='Sélectionné'),
        ),
        migrations.AddField(
            model_name='step',
            name='selected',
            field=models.BooleanField(default=False, verbose_name='Sélectionné'),
        ),
        migrations.AlterField(
            model_name='step',
            name='nature',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Type'),
        ),
    ]

# Generated by Django 2.2.3 on 2019-09-13 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('visit_report', '0022_auto_20190906_1129'),
    ]

    operations = [
        migrations.AddField(
            model_name='housing',
            name='housing_type_other_label',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Autre Type de logement'),
        ),
        migrations.AddField(
            model_name='housing',
            name='ownership_other_label',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name="Autre statut d'occupation"),
        ),
    ]
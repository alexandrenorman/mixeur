# Generated by Django 2.1.5 on 2019-02-11 18:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("visit_report", "0001_initial")]

    operations = [
        migrations.AddField(
            model_name="housing",
            name="city",
            field=models.CharField(
                blank=True, max_length=100, null=True, verbose_name="Ville"
            ),
        ),
        migrations.AddField(
            model_name="housing",
            name="postcode",
            field=models.CharField(
                blank=True, max_length=10, null=True, verbose_name="Copde postal"
            ),
        ),
    ]

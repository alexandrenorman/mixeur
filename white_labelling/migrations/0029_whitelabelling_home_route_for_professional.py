# Generated by Django 2.2.10 on 2020-08-14 10:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('white_labelling', '0028_merge_20200811_1054'),
    ]

    operations = [
        migrations.AddField(
            model_name='whitelabelling',
            name='home_route_for_professional',
            field=models.CharField(blank=True, default='Home', max_length=100, null=True, verbose_name='Route de la homepage - professionnels'),
        ),
    ]
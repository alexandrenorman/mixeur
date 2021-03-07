# Generated by Django 2.2.6 on 2019-11-18 09:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('white_labelling', '0004_auto_20191009_1214'),
    ]

    operations = [
        migrations.AddField(
            model_name='whitelabelling',
            name='newsletters_baseline',
            field=models.CharField(default='Outil de création de newsletters', max_length=100, verbose_name="Baseline de l'application newsletters"),
        ),
        migrations.AddField(
            model_name='whitelabelling',
            name='newsletters_is_active',
            field=models.BooleanField(default=True, verbose_name='Activer les newsletters'),
        ),
        migrations.AddField(
            model_name='whitelabelling',
            name='newsletters_name',
            field=models.CharField(default='Newsletters', max_length=100, verbose_name="Nom de l'application newsletters"),
        ),
    ]
# Generated by Django 2.2.10 on 2020-06-16 17:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('white_labelling', '0026_merge_20200611_1550'),
    ]

    operations = [
        migrations.AddField(
            model_name='whitelabelling',
            name='preco_immo_is_active',
            field=models.BooleanField(default=True, verbose_name="Activer les Préco'Immo"),
        ),
    ]

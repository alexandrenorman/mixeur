# Generated by Django 2.2.17 on 2021-02-18 09:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fac', '0098_auto_20210210_1426'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='accepts_newsletters',
            field=models.BooleanField(default=True, verbose_name='Accepte les newsletters'),
        ),
        migrations.AddField(
            model_name='organization',
            name='accepts_newsletters',
            field=models.BooleanField(default=True, verbose_name='Accepte les newsletters'),
        ),
    ]
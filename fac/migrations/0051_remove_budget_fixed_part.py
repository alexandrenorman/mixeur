# Generated by Django 2.2.9 on 2020-01-29 16:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fac', '0050_auto_20200127_1611'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='budget',
            name='fixed_part',
        ),
    ]
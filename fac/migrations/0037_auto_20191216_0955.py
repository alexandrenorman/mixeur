# Generated by Django 2.2.8 on 2019-12-16 08:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fac', '0036_auto_20191209_1735'),
    ]

    operations = [
        migrations.AlterField(
            model_name='folder',
            name='description',
            field=models.TextField(blank=True, default='', verbose_name='Description'),
        ),
    ]
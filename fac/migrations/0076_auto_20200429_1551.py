# Generated by Django 2.2.10 on 2020-04-29 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fac', '0075_merge_20200427_2022'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='Description'),
        ),
    ]

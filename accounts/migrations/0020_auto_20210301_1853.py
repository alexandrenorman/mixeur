# Generated by Django 2.2.17 on 2021-03-01 17:53

import accounts.models.group
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0019_auto_20210301_1843'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='address',
            field=models.CharField(blank=True, default='', max_length=200, verbose_name='Adresse'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='group',
            name='email',
            field=models.EmailField(blank=True, default='', max_length=254, verbose_name='Courriel'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='group',
            name='full_name',
            field=models.CharField(blank=True, default='', max_length=200, verbose_name='Nom complet'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='group',
            name='presentation',
            field=models.TextField(blank=True, default='', verbose_name='Présentation de la structure'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='group',
            name='profile_pic',
            field=models.ImageField(blank=True, default='', upload_to=accounts.models.group.group_directory_path),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='group',
            name='slug',
            field=models.SlugField(default='', unique='true', verbose_name='Slug'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='group',
            name='website',
            field=models.URLField(blank=True, default='', verbose_name='Site internet'),
            preserve_default=False,
        ),
    ]
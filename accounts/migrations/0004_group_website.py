# Generated by Django 2.2.6 on 2019-11-25 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20191003_1408'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='website',
            field=models.URLField(blank=True, null=True, verbose_name='Site internet'),
        ),
    ]

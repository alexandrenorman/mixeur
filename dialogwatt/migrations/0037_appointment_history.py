# Generated by Django 2.2.9 on 2020-02-25 22:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dialogwatt', '0036_auto_20200221_2119'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='history',
            field=models.TextField(default='', verbose_name='Historique des modifications'),
        ),
    ]

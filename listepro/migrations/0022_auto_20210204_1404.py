# Generated by Django 2.2.17 on 2021-02-04 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listepro', '0021_auto_20201126_1142'),
    ]

    operations = [
        migrations.AlterField(
            model_name='professional',
            name='comment',
            field=models.TextField(blank=True, max_length=2000, verbose_name='Commentaire sur le professionnel'),
        ),
    ]

# Generated by Django 2.2.10 on 2020-07-03 12:44

from django.db import migrations, models
import listepro.models.professional


class Migration(migrations.Migration):

    dependencies = [
        ('listepro', '0009_auto_20200703_1143'),
    ]

    operations = [
        migrations.AlterField(
            model_name='professional',
            name='logo',
            field=models.ImageField(blank=True, default=None, upload_to=listepro.models.professional.logo_path),
        ),
    ]

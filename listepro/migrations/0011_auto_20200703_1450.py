# Generated by Django 2.2.10 on 2020-07-03 12:50

from django.db import migrations, models
import listepro.models.professional


class Migration(migrations.Migration):

    dependencies = [
        ('listepro', '0010_auto_20200703_1444'),
    ]

    operations = [
        migrations.AlterField(
            model_name='professional',
            name='logo',
            field=models.ImageField(blank=True, default=None, null=True, upload_to=listepro.models.professional.logo_path),
        ),
    ]

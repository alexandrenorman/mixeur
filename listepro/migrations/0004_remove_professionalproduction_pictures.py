# Generated by Django 2.2.10 on 2020-06-25 09:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('listepro', '0003_auto_20200623_1807'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='professionalproduction',
            name='pictures',
        ),
    ]

# Generated by Django 2.2.7 on 2019-11-28 09:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fac', '0029_auto_20191125_1934'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fileorganization',
            name='organization',
        ),
        migrations.RemoveField(
            model_name='fileorganization',
            name='owning_group',
        ),
        migrations.RemoveField(
            model_name='fileorganization',
            name='tags',
        ),
        migrations.DeleteModel(
            name='FileContact',
        ),
        migrations.DeleteModel(
            name='FileOrganization',
        ),
    ]

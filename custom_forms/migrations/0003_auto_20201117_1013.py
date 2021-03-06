# Generated by Django 2.2.10 on 2020-11-17 09:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0014_group_address'),
        ('fac', '0083_auto_20201027_1517'),
        ('custom_forms', '0002_customform_folder_model'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customform',
            name='folder_model',
        ),
        migrations.RemoveField(
            model_name='customform',
            name='group',
        ),
        migrations.RemoveField(
            model_name='customform',
            name='project',
        ),
        migrations.AddField(
            model_name='customform',
            name='folder_models',
            field=models.ManyToManyField(related_name='custom_forms', to='fac.FolderModel', verbose_name='Modèle de dossiers'),
        ),
        migrations.AddField(
            model_name='customform',
            name='groups',
            field=models.ManyToManyField(related_name='custom_forms', to='accounts.Group', verbose_name='Groupes'),
        ),
        migrations.AddField(
            model_name='customform',
            name='projects',
            field=models.ManyToManyField(related_name='custom_forms', to='fac.Project', verbose_name='Projets'),
        ),
    ]

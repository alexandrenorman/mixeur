# Generated by Django 2.2 on 2019-06-07 12:02

import core.models
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('fac', '0004_auto_20190607_1337'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contact',
            options={'verbose_name': 'Contact', 'verbose_name_plural': 'Contacts'},
        ),
        migrations.AlterModelOptions(
            name='contactsduplicate',
            options={'verbose_name': 'Doublons de contacts', 'verbose_name_plural': 'Doublons de contacts'},
        ),
        migrations.AlterModelOptions(
            name='filecontact',
            options={'verbose_name': 'Document', 'verbose_name_plural': 'Documents'},
        ),
        migrations.AlterModelOptions(
            name='fileimport',
            options={'verbose_name': "Fichier d'import", 'verbose_name_plural': "Fichiers d'import"},
        ),
        migrations.AlterModelOptions(
            name='fileorganization',
            options={'verbose_name': 'Document', 'verbose_name_plural': 'Documents'},
        ),
        migrations.AlterModelOptions(
            name='list',
            options={'verbose_name': 'Liste de contacts', 'verbose_name_plural': 'Listes de contacts'},
        ),
        migrations.AlterModelOptions(
            name='memberoforganization',
            options={'verbose_name': "Membre d'organisations", 'verbose_name_plural': "Membres d'organisations"},
        ),
        migrations.AlterModelOptions(
            name='notecontact',
            options={'verbose_name': 'Note de contact', 'verbose_name_plural': 'Notes de contact'},
        ),
        migrations.AlterModelOptions(
            name='noteorganization',
            options={'verbose_name': 'Note de contact', 'verbose_name_plural': 'Notes de contact'},
        ),
        migrations.AlterModelOptions(
            name='organization',
            options={'verbose_name': 'Organisation', 'verbose_name_plural': 'Organisations'},
        ),
        migrations.RenameField(
            model_name='contactsduplicate',
            old_name='creation_date',
            new_name='created_at',
        ),
        migrations.RemoveField(
            model_name='contact',
            name='creation_date',
        ),
        migrations.RemoveField(
            model_name='contact',
            name='last_modification',
        ),
        migrations.RemoveField(
            model_name='filecontact',
            name='creation_date',
        ),
        migrations.RemoveField(
            model_name='fileimport',
            name='creation_date',
        ),
        migrations.RemoveField(
            model_name='fileorganization',
            name='creation_date',
        ),
        migrations.RemoveField(
            model_name='list',
            name='creation_date',
        ),
        migrations.RemoveField(
            model_name='list',
            name='last_modification',
        ),
        migrations.RemoveField(
            model_name='memberoforganization',
            name='creation_date',
        ),
        migrations.RemoveField(
            model_name='memberoforganization',
            name='last_modification',
        ),
        migrations.RemoveField(
            model_name='notecontact',
            name='creation_date',
        ),
        migrations.RemoveField(
            model_name='noteorganization',
            name='creation_date',
        ),
        migrations.RemoveField(
            model_name='organization',
            name='creation_date',
        ),
        migrations.RemoveField(
            model_name='organization',
            name='last_modification',
        ),
        migrations.AddField(
            model_name='contact',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False),
        ),
        migrations.AddField(
            model_name='contact',
            name='updated_at',
            field=core.models.AutoDateTimeField(default=django.utils.timezone.now, editable=False),
        ),
        migrations.AddField(
            model_name='filecontact',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False),
        ),
        migrations.AddField(
            model_name='filecontact',
            name='updated_at',
            field=core.models.AutoDateTimeField(default=django.utils.timezone.now, editable=False),
        ),
        migrations.AddField(
            model_name='fileimport',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False),
        ),
        migrations.AddField(
            model_name='fileimport',
            name='updated_at',
            field=core.models.AutoDateTimeField(default=django.utils.timezone.now, editable=False),
        ),
        migrations.AddField(
            model_name='fileorganization',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False),
        ),
        migrations.AddField(
            model_name='fileorganization',
            name='updated_at',
            field=core.models.AutoDateTimeField(default=django.utils.timezone.now, editable=False),
        ),
        migrations.AddField(
            model_name='list',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False),
        ),
        migrations.AddField(
            model_name='list',
            name='updated_at',
            field=core.models.AutoDateTimeField(default=django.utils.timezone.now, editable=False),
        ),
        migrations.AddField(
            model_name='memberoforganization',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False),
        ),
        migrations.AddField(
            model_name='memberoforganization',
            name='updated_at',
            field=core.models.AutoDateTimeField(default=django.utils.timezone.now, editable=False),
        ),
        migrations.AddField(
            model_name='notecontact',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False),
        ),
        migrations.AddField(
            model_name='notecontact',
            name='updated_at',
            field=core.models.AutoDateTimeField(default=django.utils.timezone.now, editable=False),
        ),
        migrations.AddField(
            model_name='noteorganization',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False),
        ),
        migrations.AddField(
            model_name='noteorganization',
            name='updated_at',
            field=core.models.AutoDateTimeField(default=django.utils.timezone.now, editable=False),
        ),
        migrations.AddField(
            model_name='organization',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False),
        ),
        migrations.AddField(
            model_name='organization',
            name='updated_at',
            field=core.models.AutoDateTimeField(default=django.utils.timezone.now, editable=False),
        ),
    ]

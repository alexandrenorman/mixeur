# Generated by Django 2.2.17 on 2020-11-26 09:45

from django.db import migrations


def postgres_migration_prep(apps, schema_editor):
    Model = apps.get_model("fac", "file")
    fields = ("url", )

    for field in fields:
        filter_param = {f"{field}__isnull": True}
        update_param = {field: ""}
        Model.objects.filter(**filter_param).update(**update_param)


class Migration(migrations.Migration):

    dependencies = [
        ('fac', '0084_auto_20201126_1013'),
    ]

    operations = [
        migrations.RunPython(postgres_migration_prep, migrations.RunPython.noop),       
    ]

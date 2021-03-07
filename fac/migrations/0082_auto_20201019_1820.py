# Generated by Django 2.2.10 on 2020-10-19 16:20

from django.db import migrations, models


def postgres_migration_prep(apps, schema_editor):
    Contact = apps.get_model("fac", "contact")
    fields = ("fax_cache", "mobile_phone_cache", "phone_cache")

    for field in fields:
        filter_param = {f"{field}__isnull": True}
        update_param = {field: ""}
        Contact.objects.filter(**filter_param).update(**update_param)


class Migration(migrations.Migration):

    dependencies = [
        ('fac', '0081_auto_20200925_1535'),
    ]

    operations = [
        migrations.RunPython(postgres_migration_prep, migrations.RunPython.noop),
    ]
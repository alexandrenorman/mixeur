# Generated by Django 2.2.17 on 2021-03-01 17:43

from django.db import migrations


def postgres_migration_prep(apps, schema_editor):
    Model = apps.get_model("accounts", "group")
    fields = (
        "address",
        "email",
        "full_name",
        "presentation",
        "profile_pic",
        "slug",
        "website",
    )

    for field in fields:
        filter_param = {f"{field}__isnull": True}
        update_param = {field: ""}
        Model.objects.filter(**filter_param).update(**update_param)



class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0018_group_ademe_id'),
    ]

    operations = [
        migrations.RunPython(postgres_migration_prep, migrations.RunPython.noop),
    ]
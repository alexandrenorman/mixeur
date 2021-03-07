# Generated by Django 2.2.10 on 2020-12-01 11:11

from django.db import migrations


def postgres_migration_prep(apps, schema_editor):
    Model = apps.get_model("white_labelling", "WhiteLabelling")
    fields = ("home_route_for_professional", )

    for field in fields:
        filter_param = {f"{field}__isnull": True}
        update_param = {field: ""}
        Model.objects.filter(**filter_param).update(**update_param)



class Migration(migrations.Migration):

    dependencies = [
        ('white_labelling', '0034_merge_20201201_1206'),
    ]

    operations = [
        migrations.RunPython(postgres_migration_prep, migrations.RunPython.noop),
    ]
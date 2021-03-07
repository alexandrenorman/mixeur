# Generated by Django 2.2.10 on 2020-11-19 12:34

from django.db import migrations


def postgres_migration_prep(apps, schema_editor):
    Contact = apps.get_model("white_labelling", "whitelabelling")
    fields = (
        "site_title",
        "site_baseline",
        "home_route",
        "home_route_for_client",
        "home_route_for_advisor",
        "home_route_for_manager",
        "home_route_for_administrator",
    )

    for field in fields:
        filter_param = {f"{field}__isnull": True}
        update_param = {field: ""}
        Contact.objects.filter(**filter_param).update(**update_param)


class Migration(migrations.Migration):

    dependencies = [
        ('white_labelling', '0031_whitelabelling_is_neutral_for_newsletters'),
    ]

    operations = [
        migrations.RunPython(postgres_migration_prep, migrations.RunPython.noop),
    ]
# Generated by Django 2.2.17 on 2020-11-25 10:20

from django.db import migrations


def postgres_migration_prep(apps, schema_editor):
    Model = apps.get_model("dialogwatt", "notification")
    fields = ("sms_message", "mail_subject", "mail_message", "chat_message")

    for field in fields:
        filter_param = {f"{field}__isnull": True}
        update_param = {field: ""}
        Model.objects.filter(**filter_param).update(**update_param)


class Migration(migrations.Migration):

    dependencies = [
        ('dialogwatt', '0049_auto_20201020_1628'),
    ]

    operations = [
        migrations.RunPython(postgres_migration_prep, migrations.RunPython.noop),
    ]

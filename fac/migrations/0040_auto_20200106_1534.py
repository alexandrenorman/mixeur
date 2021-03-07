# Generated by Django 2.2.9 on 2020-01-06 14:34

from django.db import migrations, models


def add_title_to_valorization(apps, schema_editor):
    Valorization = apps.get_model("fac", "Valorization")
    for valorization in Valorization.objects.all():
        if not valorization.title:
            valorization.title = "{} - {}".format(
                valorization.type_valorization.name, valorization.amount
            )
            valorization.save()


class Migration(migrations.Migration):

    dependencies = [
        ("fac", "0039_note_recurrences"),
    ]

    operations = [
        migrations.AddField(
            model_name="valorization",
            name="title",
            field=models.CharField(
                max_length=255, verbose_name="Titre", default=''
            ),
        ),
        migrations.RunPython(
            add_title_to_valorization, migrations.RunPython.noop
        ),
    ]

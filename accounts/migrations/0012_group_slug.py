# Generated by Django 2.2.10 on 2020-05-28 13:39

from django.db import migrations, models
from django.utils.text import slugify


def forwards_func(apps, schema_editor):
    Group = apps.get_model("accounts", "Group")
    db_alias = schema_editor.connection.alias
    for group in Group.objects.using(db_alias).all():
        group.slug = slugify(group.name)
        group.save()


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_auto_20200224_1144'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='slug',
            field=models.SlugField(null=True, unique='true', verbose_name='Slug'),
        ),
        migrations.RunPython(forwards_func, migrations.RunPython.noop),
    ]
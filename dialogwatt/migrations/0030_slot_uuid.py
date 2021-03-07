# Generated by Django 2.2.3 on 2019-07-13 21:06

from django.db import migrations, models
import uuid


def create_uuid(apps, schema_editor):
    Slot = apps.get_model('dialogwatt', 'Slot')
    for slot in Slot.objects.all():
        slot.uuid = uuid.uuid4()
        slot.save()


class Migration(migrations.Migration):

    dependencies = [
        ('dialogwatt', '0029_auto_20190713_2304'),
    ]

    operations = [
        migrations.AddField(
            model_name='slot',
            name='uuid',
            field=models.UUIDField(blank=True, null=True),
        ),
        migrations.RunPython(create_uuid),
        migrations.AlterField(
            model_name='slot',
            name='uuid',
            field=models.UUIDField(unique=True)
        )
    ]
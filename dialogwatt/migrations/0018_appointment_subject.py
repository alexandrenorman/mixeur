# Generated by Django 2.2 on 2019-05-20 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dialogwatt', '0017_appointment_place'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='subject',
            field=models.CharField(default='-', max_length=100, verbose_name='Sujet'),
            preserve_default=False,
        ),
    ]

# Generated by Django 2.2.10 on 2020-09-10 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dialogwatt', '0039_auto_20200910_0958'),
    ]

    operations = [
        migrations.AlterField(
            model_name='slot',
            name='is_active',
            field=models.BooleanField(default=True, help_text='Slot actif ?', verbose_name='active'),
        ),
    ]
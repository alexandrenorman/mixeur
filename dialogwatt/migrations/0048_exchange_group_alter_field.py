# Generated by Django 2.2.10 on 2020-10-07 16:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dialogwatt', '0047_exchange_group_datamigration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exchange',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.Group', verbose_name='Structure'),
        ),
    ]
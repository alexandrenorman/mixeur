# Generated by Django 2.2.9 on 2020-01-30 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_merge_20200212_0950'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='pilot_groups',
            field=models.ManyToManyField(blank=True, help_text='Dans FAC, les structures pilotes de cette structures', related_name='laureate_groups', to='accounts.Group', verbose_name='Structures pilotes'),
        ),
    ]
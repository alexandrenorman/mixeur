# Generated by Django 2.2.2 on 2019-06-21 14:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dialogwatt', '0020_merge_20190611_1418'),
    ]

    operations = [
        migrations.AddField(
            model_name='place',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True, verbose_name='Courriel'),
        ),
    ]

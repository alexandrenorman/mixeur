# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ('username', 'first_name', 'last_name')},
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(verbose_name='username', unique=True, max_length=30),
        ),
    ]

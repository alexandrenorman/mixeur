# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators
import accounts.models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('password', models.CharField(verbose_name='password', max_length=128)),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('is_superuser', models.BooleanField(help_text='Designates that this user has all permissions without explicitly assigning them.', default=False, verbose_name='superuser status')),
                ('username', models.CharField(verbose_name='username', max_length=30)),
                ('email', models.EmailField(unique=True, max_length=254)),
                ('first_name', models.CharField(verbose_name='first name', max_length=30)),
                ('last_name', models.CharField(verbose_name='last name', max_length=30)),
                ('is_staff', models.BooleanField(help_text='admin ?', default=False, verbose_name='staff status')),
                ('is_active', models.BooleanField(help_text='Utilisater actif ?', default=True, verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('groups', models.ManyToManyField(help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups', blank=True)),
                ('user_permissions', models.ManyToManyField(help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions', blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]

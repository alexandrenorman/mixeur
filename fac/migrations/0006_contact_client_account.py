# Generated by Django 2.2.2 on 2019-06-07 18:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('fac', '0005_auto_20190607_1402'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='client_account',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='contacts', to=settings.AUTH_USER_MODEL, verbose_name='Compte client'),
        ),
    ]

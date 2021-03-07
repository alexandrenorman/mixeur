# Generated by Django 2.2.10 on 2020-06-22 08:44

import core.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('white_labelling', '0027_whitelabelling_preco_immo_is_active'),
        ('accounts', '0012_group_slug'),
    ]

    operations = [
        migrations.CreateModel(
            name='LogUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('updated_at', core.models.AutoDateTimeField(default=django.utils.timezone.now, editable=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='log_user', to=settings.AUTH_USER_MODEL, verbose_name='Utilisateur')),
                ('white_labelling', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='log_user_wl', to='white_labelling.WhiteLabelling', verbose_name='Domaine / marque blanche')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
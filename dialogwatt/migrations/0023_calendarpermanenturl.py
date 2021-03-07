# Generated by Django 2.2.3 on 2019-07-03 10:04

import core.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dialogwatt', '0022_auto_20190701_1605'),
    ]

    operations = [
        migrations.CreateModel(
            name='CalendarPermanentUrl',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('updated_at', core.models.AutoDateTimeField(default=django.utils.timezone.now, editable=False)),
                ('unique_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('advisors', models.ManyToManyField(to=settings.AUTH_USER_MODEL, verbose_name='Conseillers')),
                ('places', models.ManyToManyField(to='dialogwatt.Place', verbose_name="Lieux d'accueil")),
                ('user', models.ForeignKey(limit_choices_to={'user_type': 'advisor'}, on_delete=django.db.models.deletion.CASCADE, related_name='calendar', to=settings.AUTH_USER_MODEL, verbose_name='Conseiller')),
            ],
            options={
                'verbose_name': 'Filtrages permanents de calendrier',
            },
        ),
    ]
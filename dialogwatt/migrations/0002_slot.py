# Generated by Django 2.1.7 on 2019-03-18 17:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0012_auto_20190308_2318'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dialogwatt', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Slot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100, verbose_name='Nom')),
                ('time_start', models.TimeField(default='00:00', verbose_name='Heure de début')),
                ('time_end', models.TimeField(default='00:00', verbose_name='Heure de fin')),
                ('visibility', models.CharField(choices=[('online', 'Rendez-vous en ligne'), ('advisor', 'Rendez-vous accessible aux conseillers uniquement'), ('without_reservation', 'Sans rendez-vous')], default='online', max_length=30, verbose_name='Visibilité')),
                ('deadline', models.IntegerField(default=24, verbose_name='Délai (en h)')),
                ('time_between_slots', models.IntegerField(default=0, verbose_name='Temps entre deux rendez-vous (en minutes)')),
                ('use_advisor_calendar', models.BooleanField(default=True, verbose_name='Gestion des agendas conseillers')),
                ('number_of_active_advisors', models.IntegerField(default=0, verbose_name='Nombre de conseillers simultanés')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Présentation du lieu')),
                ('advisors', models.ManyToManyField(limit_choices_to={'user_type': 'advisor'}, to=settings.AUTH_USER_MODEL, verbose_name='Liste de conseillers')),
                ('catchment_area', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dialogwatt.CatchmentArea', verbose_name='Zone de chalandise')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.Group', verbose_name='Structure')),
            ],
            options={
                'verbose_name': 'Créneau',
                'ordering': ('name',),
            },
        ),
    ]

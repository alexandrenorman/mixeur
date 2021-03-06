# Generated by Django 2.2.9 on 2020-02-21 20:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dialogwatt', '0035_merge_20200221_1651'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='advisor',
            field=models.ForeignKey(limit_choices_to=models.Q(('user_type', 'advisor'), ('user_type', 'superadvisor'), _connector='OR'), null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='apointments_as_advisor', to=settings.AUTH_USER_MODEL, verbose_name='Conseiller'),
        ),
        migrations.AlterField(
            model_name='calendarpermanenturl',
            name='user',
            field=models.ForeignKey(limit_choices_to=models.Q(('user_type', 'advisor'), ('user_type', 'superadvisor'), _connector='OR'), on_delete=django.db.models.deletion.CASCADE, related_name='calendar', to=settings.AUTH_USER_MODEL, verbose_name='Conseiller'),
        ),
        migrations.AlterField(
            model_name='slot',
            name='advisors',
            field=models.ManyToManyField(limit_choices_to=models.Q(('user_type', 'advisor'), ('user_type', 'superadvisor'), _connector='OR'), to=settings.AUTH_USER_MODEL, verbose_name='Liste de conseillers'),
        ),
    ]

# Generated by Django 2.2.9 on 2020-02-18 10:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fac', '0062_merge_20200217_1156'),
    ]

    operations = [
        migrations.AlterField(
            model_name='action',
            name='done_by',
            field=models.ForeignKey(blank=True, limit_choices_to=models.Q(('user_type', 'advisor'), ('user_type', 'superadvisor'), _connector='OR'), null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='actions_done', to=settings.AUTH_USER_MODEL),
        ),
    ]

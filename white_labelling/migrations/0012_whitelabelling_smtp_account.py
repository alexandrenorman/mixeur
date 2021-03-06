# Generated by Django 2.2.9 on 2020-02-07 15:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('messaging', '0002_auto_20200207_1607'),
        ('white_labelling', '0011_merge_20200204_1554'),
    ]

    operations = [
        migrations.AddField(
            model_name='whitelabelling',
            name='smtp_account',
            field=models.ForeignKey(blank=True, limit_choices_to={'group': None, 'is_active': True}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='white_labelling', to='messaging.SmtpAccount', verbose_name='Compte SMTP spécifique'),
        ),
    ]

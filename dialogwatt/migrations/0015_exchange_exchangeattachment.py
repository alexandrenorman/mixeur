# Generated by Django 2.2 on 2019-05-13 09:15

import dialogwatt.models.exchange_attachment
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import core.models


class Migration(migrations.Migration):

    dependencies = [
        ('background_task', '0002_auto_20170927_1109'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dialogwatt', '0014_auto_20190430_1356'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExchangeAttachment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('updated_at', core.models.AutoDateTimeField(default=django.utils.timezone.now, editable=False)),
                ('filecontent', models.FileField(blank=True, null=True, upload_to=dialogwatt.models.exchange_attachment.exchange_attachment_directory_path, verbose_name='Fichier')),
            ],
            options={
                'verbose_name': 'Pièce jointe',
                'verbose_name_plural': 'Pièces jointes',
                'ordering': ('-created_at',),
            },
        ),
        migrations.CreateModel(
            name='Exchange',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('updated_at', core.models.AutoDateTimeField(default=django.utils.timezone.now, editable=False)),
                ('subject', models.CharField(blank=True, max_length=100, null=True, verbose_name='Sujet')),
                ('message', models.TextField(blank=True, null=True, verbose_name='Message')),
                ('message_html', models.TextField(blank=True, null=True, verbose_name='Message')),
                ('message_type', models.CharField(choices=[('sms', 'SMS'), ('mail', 'Courriel'), ('chat', 'Chat')], default='mail', max_length=100, verbose_name='Type de message')),
                ('has_been_sent_on', models.DateTimeField(blank=True, null=True)),
                ('has_been_received_on', models.DateTimeField(blank=True, null=True)),
                ('has_been_opened_on', models.DateTimeField(blank=True, null=True)),
                ('error', models.CharField(blank=True, max_length=200, null=True, verbose_name="Message d'erreur")),
                ('attachments', models.ManyToManyField(to='dialogwatt.ExchangeAttachment', verbose_name='Fichiers joints')),
                ('background_task', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='background_task', to='background_task.Task', verbose_name='Background Task')),
                ('from_account', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='exchange_from', to=settings.AUTH_USER_MODEL, verbose_name='Expediteur')),
                ('to_account', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='exchange_to', to=settings.AUTH_USER_MODEL, verbose_name='Destinataire')),
            ],
            options={
                'verbose_name': 'Exchange',
                'ordering': ('-created_at',),
            },
        ),
    ]

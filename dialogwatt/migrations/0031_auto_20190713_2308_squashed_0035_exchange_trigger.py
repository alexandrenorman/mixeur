# Generated by Django 2.2.3 on 2019-10-03 10:26

import core.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    replaces = [('dialogwatt', '0031_auto_20190713_2308'), ('dialogwatt', '0032_auto_20190714_1005'), ('dialogwatt', '0033_auto_20190902_0946'), ('dialogwatt', '0034_auto_20190920_1708'), ('dialogwatt', '0035_exchange_trigger')]

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('dialogwatt', '0030_slot_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='slot',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
        migrations.AlterField(
            model_name='notification',
            name='trigger',
            field=models.CharField(choices=[('created_account', "Création d'un compte par le contact"), ('created_client', "Création d'un rdv par le contact"), ('changed_client', "Modification d'un rdv par le contact"), ('canceled_client', "Annulation d'un rdv par le contact"), ('created_advisor', "Création d'un rdv par le conseiller"), ('changed_advisor', "Modification d'un rdv par le conseiller"), ('canceled_advisor', "Annulation d'un rdv par le conseiller"), ('date_of_appointment', 'Échéance du rendez-vous')], max_length=100, verbose_name='Déclencheur'),
        ),
        migrations.AlterModelOptions(
            name='notification',
            options={'verbose_name': 'Notification'},
        ),
        migrations.RemoveField(
            model_name='exchange',
            name='message',
        ),
        migrations.RemoveField(
            model_name='exchange',
            name='message_html',
        ),
        migrations.AddField(
            model_name='exchange',
            name='message_mail_ascii',
            field=models.TextField(blank=True, null=True, verbose_name='Message mail plaintext'),
        ),
        migrations.AddField(
            model_name='exchange',
            name='message_mail_html',
            field=models.TextField(blank=True, null=True, verbose_name='Message mail html'),
        ),
        migrations.AddField(
            model_name='exchange',
            name='message_sms',
            field=models.TextField(blank=True, null=True, verbose_name='Message SMS'),
        ),
        migrations.AddField(
            model_name='exchange',
            name='schedule',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name="Date d'envoi programmée"),
        ),
        migrations.AddField(
            model_name='notification',
            name='mail_subject',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Sujet du MAIL'),
        ),
        migrations.AlterField(
            model_name='exchange',
            name='message_type',
            field=models.CharField(blank=True, choices=[('sms', 'SMS'), ('mail', 'Courriel'), ('chat', 'Chat')], max_length=10, null=True, verbose_name='Type de message'),
        ),
        migrations.AlterField(
            model_name='notification',
            name='advisors',
            field=models.ManyToManyField(related_name='notification', to=settings.AUTH_USER_MODEL, verbose_name='Conseillers'),
        ),
        migrations.AlterField(
            model_name='notification',
            name='chat_is_active',
            field=models.BooleanField(default=False, verbose_name='Chat actif ?'),
        ),
        migrations.AlterField(
            model_name='notification',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notification', to='accounts.Group', verbose_name='Structure'),
        ),
        migrations.AlterField(
            model_name='notification',
            name='places',
            field=models.ManyToManyField(related_name='notification', to='dialogwatt.Place', verbose_name='Lieux de conseil'),
        ),
        migrations.AlterField(
            model_name='notification',
            name='reasons',
            field=models.ManyToManyField(related_name='notification', to='dialogwatt.Reason', verbose_name='Motifs de rendez-vous'),
        ),
        migrations.CreateModel(
            name='NotificationRequested',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('updated_at', core.models.AutoDateTimeField(default=django.utils.timezone.now, editable=False)),
                ('object_id', models.PositiveIntegerField(blank=True, null=True)),
                ('content_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='notification', to='contenttypes.ContentType')),
                ('exchange', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dialogwatt.Exchange', verbose_name='Message')),
                ('notification', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dialogwatt.Notification', verbose_name='Notification')),
            ],
            options={
                'verbose_name': 'Notification demandées',
            },
        ),
        migrations.AddField(
            model_name='exchange',
            name='trigger',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Déclencheur'),
        ),
    ]
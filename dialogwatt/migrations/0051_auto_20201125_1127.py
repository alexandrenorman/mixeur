# Generated by Django 2.2.17 on 2020-11-25 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dialogwatt', '0050_remove_null'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='chat_message',
            field=models.TextField(blank=True, default='', verbose_name='Texte CHAT'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='notification',
            name='mail_message',
            field=models.TextField(blank=True, default='', verbose_name='Texte MAIL'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='notification',
            name='mail_subject',
            field=models.CharField(blank=True, default='', max_length=200, verbose_name='Sujet du MAIL'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='notification',
            name='sms_message',
            field=models.TextField(blank=True, default='', verbose_name='Texte SMS'),
            preserve_default=False,
        ),
    ]
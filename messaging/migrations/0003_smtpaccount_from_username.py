# Generated by Django 2.2.9 on 2020-02-11 07:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('messaging', '0002_auto_20200207_1607'),
    ]

    operations = [
        migrations.AddField(
            model_name='smtpaccount',
            name='from_username',
            field=models.CharField(blank=True, default='', max_length=100, verbose_name="Nom d'expéditeur affiché"),
        ),
    ]

# Generated by Django 2.2.2 on 2019-06-24 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0020_group_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='color',
            field=models.CharField(default='#888888', max_length=10, verbose_name='Color'),
        ),
    ]
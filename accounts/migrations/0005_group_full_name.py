# Generated by Django 2.2.9 on 2020-01-30 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_group_website'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='full_name',
            field=models.CharField(max_length=200, null=True, verbose_name='Nom complet'),
        ),
    ]
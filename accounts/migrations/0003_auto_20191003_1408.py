# Generated by Django 2.2.3 on 2019-10-03 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20190917_1648'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(blank=True, max_length=300, null=True, verbose_name='first name'),
        ),
    ]
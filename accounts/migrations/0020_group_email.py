# Generated by Django 2.2.2 on 2019-06-21 14:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0019_auto_20190618_2210'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True, verbose_name='Courriel'),
        ),
    ]

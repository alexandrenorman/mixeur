# Generated by Django 2.2.3 on 2019-09-17 14:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_squashed_0022_auto_20190726_1526'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='group',
            options={'verbose_name': 'Groupe', 'verbose_name_plural': 'Groupes'},
        ),
        migrations.AlterModelOptions(
            name='user',
            options={'verbose_name': 'Utilisateur'},
        ),
    ]

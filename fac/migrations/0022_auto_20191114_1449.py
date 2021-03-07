# Generated by Django 2.2.3 on 2019-11-14 13:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fac', '0021_relationbetweenorganization'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='note',
            options={'verbose_name': 'Note', 'verbose_name_plural': 'Notes'},
        ),
        migrations.AlterField(
            model_name='note',
            name='owning_group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notes', to='accounts.Group', verbose_name='Groupe propriétaire'),
        ),
    ]

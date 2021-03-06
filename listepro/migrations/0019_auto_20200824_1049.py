# Generated by Django 2.2.10 on 2020-08-24 08:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('listepro', '0018_professional_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='professional',
            name='activity_fourth',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='fourth_choice', to='listepro.Activity', verbose_name="Sélectionner un autre domaine d'activité"),
        ),
        migrations.AlterField(
            model_name='professional',
            name='activity_second',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='second_choice', to='listepro.Activity', verbose_name="Sélectionner un autre domaine d'activité"),
        ),
        migrations.AlterField(
            model_name='professional',
            name='activity_third',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='third_choice', to='listepro.Activity', verbose_name="Sélectionner un autre domaine d'activité"),
        ),
    ]

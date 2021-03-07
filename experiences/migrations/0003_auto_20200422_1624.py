# Generated by Django 2.2.11 on 2020-04-22 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('experiences', '0002_experiencesponsor_sponsortag'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='experience',
            name='sponsor',
        ),
        migrations.AddField(
            model_name='experience',
            name='sponsors',
            field=models.ManyToManyField(blank=True, related_name='experience_sponsors', to='experiences.ExperienceSponsor', verbose_name='Financeurs'),
        ),
    ]
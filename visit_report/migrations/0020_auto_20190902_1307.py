# Generated by Django 2.2.3 on 2019-09-02 11:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('visit_report', '0019_step_model_update'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workrecommendation',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
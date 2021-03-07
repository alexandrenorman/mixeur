from django.db import migrations, models

def update_scenario_names(apps, schema_editor):
    Scenario = apps.get_model('visit_report', 'Scenario')
    for scenario in Scenario.objects.all():
        if scenario.nature == 'full' :
            scenario.nature = 'primary'
        elif scenario.nature == 'partial' :
            scenario.nature = 'secondary'
        scenario.save()

class Migration(migrations.Migration):

    dependencies = [
        ('visit_report', '0016_report_housing_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scenario',
            name='nature',
            field=models.CharField(choices=[('primary', 'Scénario principal'), ('secondary', 'Scénario secondaire')], max_length=20, verbose_name='Type'),
        ),
        migrations.RunPython(update_scenario_names),
    ]

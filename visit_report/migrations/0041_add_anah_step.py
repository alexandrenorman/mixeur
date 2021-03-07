from django.db import migrations, models


def add_anah_help_in_all_reports(apps, schema_editor):
    Reports = apps.get_model('visit_report', 'Report')
    Steps = apps.get_model('visit_report', 'Step')
    for report in Reports.objects.all():
        new_step = Steps.objects.create(report=report, data="{}", category="financing", milestone="estimation", nature="anah-help", step_type="simple", selected=True)
        new_step.save()

def reverse_add_anah_help_in_all_reports(apps, schema_editor):
    Steps = apps.get_model('visit_report', 'Step')
    anah_steps = Steps.objects.filter(nature="anah-help")
    anah_steps.delete()

class Migration(migrations.Migration):

    dependencies = [
        ('visit_report', '0040_auto_20200408_1524'),
    ]

    operations = [
        migrations.RunPython(add_anah_help_in_all_reports, reverse_add_anah_help_in_all_reports),
    ]

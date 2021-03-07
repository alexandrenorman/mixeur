from django.db import migrations


def remove_cite_steps(apps, schema_editor):
    Steps = apps.get_model('visit_report', 'Step')
    Steps.objects.filter(category="financing", milestone="work-end", nature="cite").delete()


class Migration(migrations.Migration):

    dependencies = [
        ('visit_report', '0050_add_prime_renov_step'),
    ]

    operations = [
        migrations.RunPython(remove_cite_steps),
    ]

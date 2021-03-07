from django.db import migrations


def add_prime_renov_step_in_all_reports(apps, schema_editor):
    Reports = apps.get_model('visit_report', 'Report')
    Steps = apps.get_model('visit_report', 'Step')
    for report in Reports.objects.all():
        new_step = Steps.objects.create(report=report, data="{}", category="financing", milestone="estimation", nature="prime-renov", step_type="simple", selected=True)
        new_step.save()


def reverse_prime_renov_step_in_all_reports(apps, schema_editor):
    Steps = apps.get_model('visit_report', 'Step')
    anah_steps = Steps.objects.filter(nature="prime-renov")
    anah_steps.delete()


def add_prime_renov_financial_aid_in_all_reports(apps, schema_editor):
    Scenarios = apps.get_model('visit_report', 'Scenario')
    FinancialAids = apps.get_model('visit_report', 'FinancialAid')
    for scenario in Scenarios.objects.all():
        if not scenario.financialaid_set.filter(nature='prime-renov').exists() :
            new_financial_aid = FinancialAids.objects.create(scenario=scenario, nature='prime-renov')
            new_financial_aid.save()


def reverse_prime_renov_financial_aid_in_all_reports(apps, schema_editor):
    FinancialAids = apps.get_model('visit_report', 'FinancialAid')
    action_logement = FinancialAids.objects.filter(nature="prime-renov")
    action_logement.delete()


def add_action_logement_financial_aid_in_all_reports(apps, schema_editor):
    Scenarios = apps.get_model('visit_report', 'Scenario')
    FinancialAids = apps.get_model('visit_report', 'FinancialAid')
    for scenario in Scenarios.objects.all():
        new_financial_aid = FinancialAids.objects.create(scenario=scenario, nature='action-logement')
        new_financial_aid.save()


def reverse_action_logement_financial_aid_in_all_reports(apps, schema_editor):
    FinancialAids = apps.get_model('visit_report', 'FinancialAid')
    action_logement = FinancialAids.objects.filter(nature="action-logement")
    action_logement.delete()


class Migration(migrations.Migration):

    dependencies = [
        ('visit_report', '0049_auto_20201019_1610'),
    ]

    operations = [
        migrations.RunPython(add_prime_renov_step_in_all_reports, reverse_prime_renov_step_in_all_reports),
        migrations.RunPython(add_prime_renov_financial_aid_in_all_reports, reverse_prime_renov_financial_aid_in_all_reports),
        migrations.RunPython(add_action_logement_financial_aid_in_all_reports, reverse_action_logement_financial_aid_in_all_reports),
    ]

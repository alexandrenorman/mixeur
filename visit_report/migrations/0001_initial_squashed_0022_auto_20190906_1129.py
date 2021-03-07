# Generated by Django 2.2.3 on 2019-09-17 14:10

import core.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


# Functions from the following migrations need manual copying.
# Move them and any dependencies into this file, then update the
# RunPython operations to refer to the local versions:
# visit_report.migrations.0017_update_scenario_names
def update_scenario_names(apps, schema_editor):
    Scenario = apps.get_model('visit_report', 'Scenario')
    for scenario in Scenario.objects.all():
        if scenario.nature == 'full' :
            scenario.nature = 'primary'
        elif scenario.nature == 'partial' :
            scenario.nature = 'secondary'
        scenario.save()


class Migration(migrations.Migration):

    replaces = [('visit_report', '0001_initial'), ('visit_report', '0002_auto_20190211_1958'), ('visit_report', '0003_auto_20190221_0954'), ('visit_report', '0004_auto_20190221_1011'), ('visit_report', '0005_auto_20190225_2252'), ('visit_report', '0006_auto_20190228_2116'), ('visit_report', '0007_auto_20190228_2350'), ('visit_report', '0008_auto_20190301_0046'), ('visit_report', '0009_auto_20190515_1327'), ('visit_report', '0010_auto_20190711_1101'), ('visit_report', '0011_auto_20190713_0054'), ('visit_report', '0012_auto_20190717_1751'), ('visit_report', '0013_auto_20190726_1237'), ('visit_report', '0014_auto_20190731_1529'), ('visit_report', '0015_auto_20190802_1512'), ('visit_report', '0016_report_housing_comment'), ('visit_report', '0017_update_scenario_names'), ('visit_report', '0018_housing_year'), ('visit_report', '0019_step_model_update'), ('visit_report', '0020_auto_20190902_1307'), ('visit_report', '0021_report_visit_date'), ('visit_report', '0022_auto_20190906_1129')]

    dependencies = [
        ('accounts', '0021_user_color'),
        ('accounts', '0011_remove_user_address'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Housing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(blank=True, max_length=200, null=True, verbose_name='Adresse')),
                ('housing_type', models.CharField(choices=[('house', 'Maison'), ('condo', 'Copropriété'), ('building', 'Immeuble'), ('flat', 'Appartement'), ('other', 'Autre')], default='house', max_length=20, verbose_name='Type de logement')),
                ('ownership', models.CharField(choices=[('tenant', 'Locataire'), ('owner', 'Propriétaire'), ('other', 'Autre')], default='owner', max_length=20, verbose_name='Propriété')),
                ('area', models.PositiveIntegerField(default=0, verbose_name='Superficie (en m²)')),
                ('occupants_number', models.PositiveIntegerField(default=0, verbose_name="Nombre d'occupants")),
                ('note', models.TextField(blank=True, null=True, verbose_name='Notes')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='housing', to=settings.AUTH_USER_MODEL, verbose_name='Contact')),
                ('city', models.CharField(blank=True, max_length=100, null=True, verbose_name='Ville')),
                ('postcode', models.CharField(blank=True, max_length=8, null=True, verbose_name='Code postal')),
                ('inseecode', models.CharField(blank=True, max_length=8, null=True, verbose_name='Code INSEE')),
                ('is_main_address', models.BooleanField(default=False, verbose_name='Utiliser comme adresse principale')),
                ('groups', models.ManyToManyField(to='accounts.Group', verbose_name='Structures attachées à ce logement')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('updated_at', core.models.AutoDateTimeField(default=django.utils.timezone.now, editable=False)),
            ],
            options={
                'verbose_name': 'Housing',
            },
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fiscal_income', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=8, null=True, verbose_name='Revenu fiscal de référence')),
                ('consumption_information_source', models.CharField(blank=True, choices=[('bill', 'Facture'), ('dpe', 'DPE'), ('declarative', 'Déclaratif'), ('estimative', 'Estimatif'), ('unavailable', 'Non disponible')], max_length=30, null=True, verbose_name="Source d'information")),
                ('consumption_heating', models.PositiveIntegerField(default=0, verbose_name='Chauffage')),
                ('consumption_hot_water', models.PositiveIntegerField(blank=True, default=0, verbose_name='Eau chaude sanitaire')),
                ('consumption_heating_hot_water', models.BooleanField(default=False, verbose_name='Chauffage et eau chaude groupés')),
                ('consumption_electricity', models.PositiveIntegerField(default=0, verbose_name='Electricité hors chauffage')),
                ('dpe', models.CharField(blank=True, choices=[('a', 'Classe A'), ('b', 'Classe B'), ('c', 'Classe C'), ('d', 'Classe D'), ('e', 'Classe E'), ('-', 'Non connu')], default='-', max_length=2, verbose_name='DPE')),
                ('consumption_comment', models.TextField(blank=True, null=True, verbose_name="Commentaire sur consommations d'énergie")),
                ('house_inventory_comment', models.TextField(blank=True, null=True, verbose_name="Commentaire sur l'état des lieux du logement")),
                ('conclusion_comment', models.TextField(blank=True, null=True, verbose_name='Commentaire sur la conclusion du rapport')),
                ('advisor', models.ForeignKey(blank=True, limit_choices_to={'user_type': 'advisor'}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='report', to=settings.AUTH_USER_MODEL, verbose_name='Conseiller')),
                ('group', models.ForeignKey(blank=True, limit_choices_to={'is_admin': False}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='report', to='accounts.Group', verbose_name='Structure signataire')),
                ('housing', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='report', to='visit_report.Housing', verbose_name='Logement associé')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('updated_at', core.models.AutoDateTimeField(default=django.utils.timezone.now, editable=False)),
                ('housing_comment', models.TextField(blank=True, null=True, verbose_name="Commentaire sur l'identité du logement")),
            ],
            options={
                'verbose_name': 'Rapport de visite',
                'verbose_name_plural': 'Rapports de visite',
            },
        ),
        migrations.CreateModel(
            name='Scenario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nature', models.CharField(choices=[('primary', 'Scénario principal'), ('secondary', 'Scénario secondaire')], max_length=20, verbose_name='Type')),
                ('custom_summary', models.CharField(blank=True, max_length=500, null=True, verbose_name='Résumé personnalisé')),
                ('report', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='scenario', to='visit_report.Report', verbose_name='Rapport')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('updated_at', core.models.AutoDateTimeField(default=django.utils.timezone.now, editable=False)),
            ],
            options={
                'verbose_name': 'Scénario',
            },
        ),
        migrations.CreateModel(
            name='Face',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('evaluation', models.PositiveIntegerField(default=2, verbose_name='Evaluation')),
                ('comment', models.CharField(blank=True, max_length=200, null=True, verbose_name='Commentaire')),
                ('insulation_nature', models.CharField(blank=True, choices=[('synthetic', 'Synthétique'), ('mineral', 'Minéral'), ('biosourced', 'Biosourcé'), ('undetermined', 'Non déterminé')], max_length=20, null=True, verbose_name="Nature de l'isolant")),
                ('nature', models.CharField(choices=[('wall', 'Mur'), ('floor', 'Sol'), ('roof', 'Toiture'), ('window', 'Fenêtre')], max_length=20, verbose_name='Type')),
                ('data', models.CharField(blank=True, max_length=1000, null=True, verbose_name='Autres données')),
                ('report', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='face', to='visit_report.Report', verbose_name='Rapport')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('updated_at', core.models.AutoDateTimeField(default=django.utils.timezone.now, editable=False)),
            ],
            options={
                'verbose_name': 'Paroi',
            },
        ),
        migrations.CreateModel(
            name='FinancialAid',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.PositiveIntegerField(default=0, verbose_name='Montant')),
                ('selected', models.BooleanField(default=False, verbose_name='Sélectionnée')),
                ('custom_label', models.CharField(blank=True, max_length=50, null=True, verbose_name='Label personnalisé')),
                ('scenario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='visit_report.Scenario', verbose_name='Scénario')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('updated_at', core.models.AutoDateTimeField(default=django.utils.timezone.now, editable=False)),
            ],
            options={
                'verbose_name': 'Aide financière',
                'verbose_name_plural': 'Aides financières',
            },
        ),
        migrations.CreateModel(
            name='Financing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.PositiveIntegerField(default=0, verbose_name='Montant')),
                ('selected', models.BooleanField(default=False, verbose_name='Sélectionné')),
                ('scenario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='visit_report.Scenario', verbose_name='Scénario')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('updated_at', core.models.AutoDateTimeField(default=django.utils.timezone.now, editable=False)),
            ],
            options={
                'verbose_name': 'Financement',
            },
        ),
        migrations.CreateModel(
            name='ScenarioSummary',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('scenario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='visit_report.Scenario', verbose_name='Scénario')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('updated_at', core.models.AutoDateTimeField(default=django.utils.timezone.now, editable=False)),
            ],
            options={
                'verbose_name': 'Résumé du scénario',
                'verbose_name_plural': 'Résumés des scénarii',
            },
        ),
        migrations.CreateModel(
            name='Step',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(blank=True, choices=[('estimation', 'Réalisation du devis'), ('estimation_signature', 'Signature du devis'), ('work_beginning', 'Début des travaux'), ('work_end', 'Fin des travaux')], max_length=25, null=True, verbose_name='Catégorie')),
                ('order', models.PositiveIntegerField(default=0, verbose_name='Ordre')),
                ('nature', models.CharField(choices=[('simple', 'Simple'), ('info', 'Avec infos supplémentaires'), ('contact', 'Avec coordonnées de contact'), ('field', 'Avec saisie libre')], default='regular', max_length=25, verbose_name='Type')),
                ('data', models.TextField(blank=True, null=True, verbose_name='Autres données')),
                ('report', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='step', to='visit_report.Report', verbose_name='Rapport')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('updated_at', core.models.AutoDateTimeField(default=django.utils.timezone.now, editable=False)),
            ],
            options={
                'verbose_name': 'Etape',
            },
        ),
        migrations.CreateModel(
            name='System',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nature', models.CharField(choices=[('heating-main', 'Production de chauffage'), ('emitter', 'Emetteur'), ('controler', 'Régulation'), ('hot-water', "Production d'eau chaude"), ('heating-extra', "Chauffage d'appoint"), ('ventilation', 'Ventilation'), ('photovoltaic', 'Photovoltaïque')], max_length=20, verbose_name='Type')),
                ('data', models.TextField(blank=True, null=True, verbose_name='Autres données')),
                ('report', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='system', to='visit_report.Report', verbose_name='Rapport')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('updated_at', core.models.AutoDateTimeField(default=django.utils.timezone.now, editable=False)),
            ],
            options={
                'verbose_name': 'Système',
            },
        ),
        migrations.CreateModel(
            name='WorkRecommendation',
            fields=[
                ('id', models.PositiveIntegerField(default=1, primary_key=True, serialize=False, verbose_name='Id')),
                ('category', models.CharField(choices=[('enveloppe', 'Enveloppe'), ('systems', 'Système'), ('others', 'Autres'), ('eco-gestures', 'Eco gestes')], max_length=25, verbose_name='Catégorie')),
                ('nature', models.CharField(choices=[('roof-insulation', 'Isolation de la toiture'), ('wall-insulation', 'Isolation des murs'), ('floor-insulation', 'Isolation du plancher bas'), ('carpentry-replacement', 'Remplacement des menuiseries'), ('ventilation', 'VMC'), ('heating-production', 'Production de chaleur'), ('heating-emitter', 'Production de chaleur'), ('hot-water-production', "Production d'eau chaude sanitaire"), ('heating-control', 'Régulation du système de chauffage'), ('photovoltaic', 'Installation de panneaux solaires photovoltaïques'), ('eco-gestures', 'Eco gestes'), ('calorifuge', 'Calorifuge'), ('water-tank-insulation', 'water-tank-insulation'), ('additional-costs', 'Frais supplémentaires')], max_length=50, verbose_name='Type')),
                ('name', models.CharField(blank=True, max_length=50, null=True, verbose_name='Nom')),
                ('selected', models.BooleanField(default=False, verbose_name='Sélectionné')),
                ('cost', models.PositiveIntegerField(default=0, verbose_name='Coût estimé')),
                ('comment', models.TextField(blank=True, null=True, verbose_name='Commentaires')),
                ('selected_scenario_alt', models.BooleanField(default=False, verbose_name='Sélectionné dans le scénario partiel')),
                ('data', models.TextField(blank=True, null=True, verbose_name='Autres données')),
                ('report', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='work_recommendation', to='visit_report.Report', verbose_name='Rapport')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('updated_at', core.models.AutoDateTimeField(default=django.utils.timezone.now, editable=False)),
            ],
            options={
                'verbose_name': 'Recommendation de travaux',
                'verbose_name_plural': 'Recommendations de travaux',
            },
        ),
        migrations.RunPython(
            code=update_scenario_names,
        ),
        migrations.AddField(
            model_name='housing',
            name='year',
            field=models.CharField(blank=True, max_length=8, null=True, verbose_name='Année de construction'),
        ),
        migrations.RenameField(
            model_name='step',
            old_name='category',
            new_name='milestone',
        ),
        migrations.AddField(
            model_name='step',
            name='category',
            field=models.CharField(blank=True, choices=[('financing', 'Quand demander les aides financières ?'), ('contacts', 'Qui contacter ?')], max_length=25, null=True, verbose_name='Catégorie'),
        ),
        migrations.AlterField(
            model_name='step',
            name='nature',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Nom'),
        ),
        migrations.AlterField(
            model_name='step',
            name='milestone',
            field=models.CharField(blank=True, choices=[('estimation', 'Réalisation du devis'), ('estimation-signature', 'Signature du devis'), ('work-beginning', 'Début des travaux'), ('work-end', 'Fin des travaux')], max_length=25, null=True, verbose_name='Etape du projet'),
        ),
        migrations.AddField(
            model_name='step',
            name='step_type',
            field=models.CharField(choices=[('simple', 'Simple'), ('info', 'Avec infos supplémentaires'), ('contact', 'Avec coordonnées de contact'), ('field', 'Avec saisie libre')], default='regular', max_length=25, verbose_name='Type'),
        ),
        migrations.AlterField(
            model_name='workrecommendation',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AddField(
            model_name='report',
            name='visit_date',
            field=models.DateField(default=django.utils.timezone.now, editable=False, verbose_name='Date de la visite'),
        ),
        migrations.AddField(
            model_name='financialaid',
            name='nature',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Type'),
        ),
        migrations.AddField(
            model_name='financing',
            name='nature',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Type'),
        ),
        migrations.AddField(
            model_name='scenariosummary',
            name='nature',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Type'),
        ),
        migrations.AddField(
            model_name='scenariosummary',
            name='selected',
            field=models.BooleanField(default=False, verbose_name='Sélectionné'),
        ),
        migrations.AddField(
            model_name='step',
            name='selected',
            field=models.BooleanField(default=False, verbose_name='Sélectionné'),
        ),
        migrations.AlterField(
            model_name='step',
            name='nature',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Type'),
        ),
    ]

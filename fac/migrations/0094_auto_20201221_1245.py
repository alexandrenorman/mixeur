# Generated by Django 2.2.17 on 2020-12-21 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fac', '0093_merge_20201211_1648'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='type_of_organization',
            field=models.CharField(choices=[('AgenceImmobiliere', 'Agence Immobilière'), ('Architecte', 'Architecte'), ('Association', 'Association'), ('Assureur', 'Assureur'), ('BailleurSocial', 'Bailleur social'), ('Banque', 'Banque'), ('BureauEtudes', "Bureau d'études"), ('ChambreConsulaire', 'Chambre consulaire'), ('Commune', 'Commune'), ('Courtier', 'Courtier'), ('Departement', 'Département'), ('Diagnostiqueur', 'Diagnostiqueur'), ('EnseignementFormation', 'Enseignement et formation'), ('Entreprise', 'Entreprise'), ('EntrepriseRealisation', 'Entreprise de la réalisation'), ('EPCI', 'EPCI'), ('Etat', 'État et établissements publics'), ('Fabricant', 'Fabricant'), ('Fondation', 'Fondation'), ('MaitreOeuvre', "Maître d'œuvre"), ('MaitreOuvrage', "Maître d'ouvrage"), ('MarchandDeBien', 'Marchand de bien'), ('Media', 'Média'), ('Notaire', 'Notaire'), ('OperateurEnEtancheitAir', "Opérateur en étanchéité à l'air"), ('PartenaireHabitat', 'Partenaire habitat'), ('Programmiste', 'Programmiste'), ('Region', 'Région'), ('SyndicatDeCoproprietaire', 'Syndicat de copropriétaire'), ('SyndicatEnergie', "Syndicat d'énergie"), ('SyndicatMixte', 'Syndicat Mixte'), ('UNKNOWN', 'Autre')], default='UNKNOWN', max_length=50, verbose_name="Type d'organisation"),
        ),
    ]

# -*- coding: utf-8 -*-

from django.utils.translation import ugettext_lazy as _

CIVILITIES = (("-", _("Non précisé")), ("M.", _("M.")), ("Mme", _("Mme")))

TYPE_OF_ORGANIZATION = (
    ("AgenceImmobiliere", "Agence Immobilière"),
    ("Architecte", "Architecte"),
    ("Association", "Association"),
    ("Assureur", "Assureur"),
    ("BailleurSocial", "Bailleur social"),
    ("Banque", "Banque"),
    ("BureauEtudes", "Bureau d'études"),
    ("ChambreConsulaire", "Chambre consulaire"),
    ("Commune", "Commune"),
    ("Courtier", "Courtier"),
    ("Departement", "Département"),
    ("Diagnostiqueur", "Diagnostiqueur"),
    ("EnseignementFormation", "Enseignement et formation"),
    ("Entreprise", "Entreprise"),
    ("EntrepriseRealisation", "Entreprise de la réalisation"),
    ("EPCI", "EPCI"),
    ("Etat", "État et établissements publics"),
    ("Fabricant", "Fabricant"),
    ("Fondation", "Fondation"),
    ("MaitreOeuvre", "Maître d'œuvre"),
    ("MaitreOuvrage", "Maître d'ouvrage"),
    ("MarchandDeBien", "Marchand de bien"),
    ("Media", "Média"),
    ("Notaire", "Notaire"),
    ("OperateurEnEtancheitAir", "Opérateur en étanchéité à l'air"),
    ("PartenaireHabitat", "Partenaire habitat"),
    ("Programmiste", "Programmiste"),
    ("Region", "Région"),
    ("SyndicatDeCoproprietaire", "Syndicat de copropriétaire"),
    ("SyndicatEnergie", "Syndicat d'énergie"),
    ("SyndicatMixte", "Syndicat Mixte"),
    ("UNKNOWN", "Autre"),
)

PERM = (
    ("group", "Limité au groupe"),
    ("ro", "Visible par tous, modifiable uniquement par les membres du groupe"),
    ("rw", "Modifiable par tous"),
)

ACTIMMO_TAGS_PREFIXES = {"BAN-", "COU-", "IMM-", "NOT-"}

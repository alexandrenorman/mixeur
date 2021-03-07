"""
Ce script permet de générer tous les modèles de dossiers, actions, etc, pour
le programme SARE de démonstration.

Pour le lancer :

    inv run -c "populate_sare"

S'il rencontre un problème à l'exécution, rien ne sera créé.

Pour supprimer tout ce qui a été créé : supprimer le projet Sare, ainsi que
le type de valorisation SARE.
"""

import datetime
import json
from enum import Enum, auto

from django.core.management.base import BaseCommand
from django.db import transaction

from custom_forms.models import (
    CustomForm,
)

from fac.models import (
    ActionModel,
    CategoryModel,
    FolderModel,
    Period,
    Project,
    Status,
    TypeValorization,
    Valorization,
)


class ActionType(Enum):
    ONE = auto()
    ONE_OR_MORE = auto()
    ZERO_OR_MORE = auto()


class ActionBooleans(Enum):
    MESSAGE_REQUIRED = auto()
    FILE_REQUIRED = auto()
    CONTACT_REQUIRED = auto()
    COEFFICIENT_ENABLED = auto()


class Command(BaseCommand):
    help = "Create models for SARE organizations"  # NOQA: A003

    @transaction.atomic  # NOQA: CFQ001
    def handle(self, *args, **options):
        project, _ = Project.objects.get_or_create(name="Programme SARE")

        print("Creating contact custom forms for project")
        create_custom_forms_for_project_on_contact(project)

        print("Creating Folder models…")
        menages, copros, tertiaire = map_first(
            [
                FolderModel.objects.get_or_create(
                    name=name, defaults={"icon": icon, "project": project}
                )
                for name, icon in [
                    ("Parcours SARE - Ménages", "home-lg"),
                    ("Parcours SARE - Syndicats de copropriétaires", "city"),
                    ("Parcours SARE - Petit tertiaire privé", "warehouse"),
                ]
            ]
        )

        print("Creating contact custom forms for folder model tertiaire")
        create_custom_forms_for_folder_on_organization(tertiaire)

        print("Creating valorization types…")
        sare_valorization, _ = TypeValorization.objects.update_or_create(
            name="Tarifs uniques du SARE"
        )

        project.type_valorizations.add(sare_valorization)

        sare_period, _ = Period.objects.update_or_create(
            name="SARE - 2020",
            defaults={
                "date_start": datetime.date(year=2020, month=1, day=1),
                "date_end": datetime.date(year=2020, month=12, day=31),
            },
        )

        ###########
        # Ménages #
        ###########

        # Statuts
        print(f"Filling folder model : {menages.name}")
        [
            menages_initial,
            menages_conseille,
            menages_travaux_en_cours,
            menages_termine,
        ] = create_status(
            menages,
            ["Projet à initier", "Conseillé", "Travaux en cours", "Projet terminé"],
        )

        # Categories
        [menages_actes_sare, menages_autres] = create_category_models(
            menages, ["Actes du programme SARE", "Autres"]
        )

        # Actions
        [
            menages_infos,
            menages_conseil_perso,
            menages_audit,
            menages_accompagnement_real,
            menages_accompagnement_suivi,
            menages_moe,
            menages_email,
            menages_projet_termine,
        ] = create_action_models(
            [
                (
                    menages_actes_sare,
                    "A1 - Information de premier niveau",
                    """Information générique.""",
                    ActionType.ONE_OR_MORE,
                    menages_conseille,
                    (),
                ),
                (
                    menages_actes_sare,
                    "A2 - Conseil personnalisé",
                    """Important : vous devez produire un compte-rendu pour valider cet acte, et devez stocker cette pièce en cas de contrôle. Vous pouvez utiliser le champ "Pièce jointe" pour cela.""",  # NOQA: E501
                    ActionType.ONE_OR_MORE,
                    menages_conseille,
                    (),
                ),
                (
                    menages_actes_sare,
                    "A3 - Réalisation d'audits énergétiques",
                    """Merci de joindre le/les audits réalisés.""",
                    ActionType.ONE,
                    menages_conseille,
                    (),
                ),
                (
                    menages_actes_sare,
                    "A4 - Accompagnement dans la réalisation des travaux",
                    """Accompagnement des ménages pour la réalisation de leurs travaux de rénovation globale""",
                    ActionType.ONE,
                    menages_travaux_en_cours,
                    (),
                ),
                (
                    menages_actes_sare,
                    "A4 bis - Accompagnement et suivi des travaux",
                    """Accompagnement des ménages et suivi des travaux pour la réalisation de leurs travaux de rénovation globale""",  # NOQA: E501
                    ActionType.ONE,
                    menages_travaux_en_cours,
                    (),
                ),
                (
                    menages_actes_sare,
                    "A5 - Prestation maîtrise d'oeuvre",
                    """Réalisation de prestation de maitrise d'œuvre pour leurs travaux de rénovations globales""",
                    ActionType.ONE,
                    menages_travaux_en_cours,
                    (),
                ),
                (
                    menages_autres,
                    "Commentaire",
                    "",
                    ActionType.ZERO_OR_MORE,
                    None,
                    (),
                ),
                (
                    menages_autres,
                    "Projet terminé",
                    "",
                    ActionType.ONE,
                    menages_termine,
                    (),
                ),
            ]
        )

        #######################
        # Syndicats de copros #
        #######################

        # Statuts
        print(f"Filling folder model : {copros.name}")
        [
            copros_initial,
            copros_conseille,
            copros_travaux_en_cours,
            copros_termine,
        ] = create_status(
            copros,
            ["Projet à initier", "Conseillé", "Travaux en cours", "Projet terminé"],
        )

        # Categories
        [copros_actes_sare, copros_autres] = create_category_models(
            copros, ["Actes du programme SARE", "Autres"]
        )

        # Actions
        [
            copros_infos,
            copros_conseil_perso,
            copros_audit,
            copros_accompagnement_real,
            copros_accompagnement_suivi,
            copros_moe,
            copros_email,
            copros_projet_termine,
        ] = create_action_models(
            [
                (
                    copros_actes_sare,
                    "A1 - Information de premier niveau",
                    """Information générique.""",
                    ActionType.ONE_OR_MORE,
                    copros_conseille,
                    (),
                ),
                (
                    copros_actes_sare,
                    "A2 - Conseil personnalisé",
                    """Important : vous devez produire un compte-rendu pour valider cet acte, et devez stocker cette pièce en cas de contrôle. Vous pouvez utiliser le champ "Pièce jointe" pour cela.""",  # NOQA: E501
                    ActionType.ONE_OR_MORE,
                    copros_conseille,
                    (),
                ),
                (
                    copros_actes_sare,
                    "A3 - Réalisation d'audits énergétiques",
                    """Merci de joindre le/les audits réalisés.""",
                    ActionType.ONE,
                    copros_conseille,
                    (),
                ),
                (
                    copros_actes_sare,
                    "A4 - Accompagnement dans la réalisation des travaux",
                    """Accompagnement des ménages pour la réalisation de leurs travaux de rénovation globale""",
                    ActionType.ONE,
                    copros_travaux_en_cours,
                    (),
                ),
                (
                    copros_actes_sare,
                    "A4 bis - Accompagnement et suivi des travaux",
                    """Accompagnement des ménages et suivi des travaux pour la réalisation de leurs travaux de rénovation globale""",  # NOQA: E501
                    ActionType.ONE,
                    copros_travaux_en_cours,
                    (),
                ),
                (
                    copros_actes_sare,
                    "A5 - Prestation maîtrise d'oeuvre",
                    """Réalisation de prestation de maitrise d'œuvre pour leurs travaux de rénovations globales""",
                    ActionType.ONE,
                    copros_travaux_en_cours,
                    (),
                ),
                (
                    copros_autres,
                    "Commentaire",
                    "",
                    ActionType.ZERO_OR_MORE,
                    None,
                    (),
                ),
                (
                    copros_autres,
                    "Projet terminé",
                    "",
                    ActionType.ONE,
                    copros_termine,
                    (),
                ),
            ]
        )

        ###################
        # Petit tertiaire #
        ###################

        # Statuts
        print(f"Filling folder model : {tertiaire.name}")
        [tertiaire_initial, tertiaire_conseille] = create_status(
            tertiaire, ["Projet à initier", "Conseillé"]
        )

        # Categories
        [tertiaire_actes_sare, tertiaire_autres] = create_category_models(
            tertiaire, ["Actes du programme SARE", "Autres"]
        )

        # Actions
        [
            tertiaire_infos,
            tertiaire_conseil_perso,
            tertiaire_email,
        ] = create_action_models(
            [
                (
                    tertiaire_actes_sare,
                    "B1 - Information de premier niveau",
                    """Information générique.""",
                    ActionType.ONE_OR_MORE,
                    tertiaire_conseille,
                    (ActionBooleans.CONTACT_REQUIRED,),
                ),
                (
                    tertiaire_actes_sare,
                    "B2 - Conseil personnalisé aux entreprises",
                    "",
                    ActionType.ONE_OR_MORE,
                    tertiaire_conseille,
                    (ActionBooleans.CONTACT_REQUIRED,),
                ),
                (
                    tertiaire_autres,
                    "Commentaire",
                    "",
                    ActionType.ZERO_OR_MORE,
                    None,
                    (),
                ),
            ]
        )

        #################
        # Valorizations #
        #################

        for actions, valorizations in [
            ([menages_infos, copros_infos], [(sare_valorization, 8)]),
            ([menages_conseil_perso, copros_conseil_perso], [(sare_valorization, 50)]),
            ([menages_audit], [(sare_valorization, 200)]),
            ([menages_accompagnement_real], [(sare_valorization, 800)]),
            ([menages_accompagnement_suivi, menages_moe], [(sare_valorization, 1200)]),
            ([copros_audit, copros_accompagnement_real], [(sare_valorization, 4000)]),
            ([copros_accompagnement_suivi, copros_moe], [(sare_valorization, 8000)]),
            ([tertiaire_infos], [(sare_valorization, 16)]),
            ([tertiaire_conseil_perso], [(sare_valorization, 400)]),
        ]:
            for action in actions:
                action.valorizations.set(
                    map_first(
                        [
                            Valorization.objects.get_or_create(
                                title=f"{action.category_model.folder_model.name} — {action.name} — "
                                + f"{type_valorization.name}",
                                defaults={
                                    "act": True,
                                    "amount": amount,
                                    "type_valorization": type_valorization,
                                    "period": sare_period,
                                },
                            )
                            for type_valorization, amount in valorizations
                        ]
                    )
                )

        ################
        # Custom Forms #
        ################
        print("Creating CustomForms : Actions")

        [
            sare_A1,
            sare_A2,
            sare_A3,
            sare_A4,
            sare_A4bis,
            sare_A5,
            sare_B1,
            sare_B2,
        ] = create_custom_forms_actions(
            [
                (
                    (menages_infos, copros_infos),
                    "Informations parcours SARE Ménages A1",
                    """
{
  "label": "Informations parcours SARE",
  "content": [
    {

      "id": "d_034",
      "type": "SelectList",
      "label": "Type d’information",
      "isAbstract": true,
      "icon": "info-circle",
      "choices": {
        "Information financière": "Information financière",
        "Information juridique": "Information juridique",
        "Information sociale": "Information sociale",
        "Information technique": "Information technique"
      },
      "helptext": "",
      "mandatory": true,
      "multiple": true
    },
    {
      "id": "d_035",
      "type": "SelectList",
      "label": "Nature de l’information",
      "isAbstract": true,
      "icon": "info-circle",
      "choices": {
        "Aides financières": "Aides financières",
        "Amélioration légère": "Amélioration légère",
        "Compréhension des factures d'énergie": "Compréhension des factures d'énergie",
        "Construction": "Construction",
        "Demande à caractère économique et financier": "Demande à caractère économique et financier",
        "Démarchage": "Démarchage",
        "ENR": "ENR",
        "Eco-gestes (économie d'eau, d'énergie...)": "Eco-gestes (économie d'eau, d'énergie...)",
        "Informations générales": "Informations générales",
        "Offres à 1€": "Offres à 1€",
        "Question techniques": "Question techniques",
        "Réglementation/Législation": "Réglementation/Législation",
        "Rénovation lourde": "Rénovation lourde",
        "Thermographie": "Thermographie",
        "Transport et mobilité": "Transport et mobilité"
      },
      "helptext": "",
      "multiple": true,
      "mandatory": false
    },
    {
      "id": "d_036",
      "type": "TextArea",
      "label": "Question",
      "helptext": "",
      "mandatory": true
    },
    {
      "id": "d_037",
      "type": "TextArea",
      "label": "Réponse",
      "helptext": "",
      "mandatory": true
    }
  ]
}
                    """,
                ),
                (
                    (menages_conseil_perso, copros_conseil_perso),
                    "Informations parcours SARE Ménages A2",
                    """
{
  "label": "Informations parcours SARE",
  "content": [
    {
      "id": "d_043",
      "type": "SelectList",
      "label": "Poursuite de service envisagée",
      "isAbstract": true,
      "icon": "arrow-alt-circle-right",
      "choices": {
        "Accompagnement à la réalisation des travaux": "Accompagnement à la réalisation des travaux",
        "Action Logement": "Action Logement",
        "HMS": "HMS - Habiter Mieux Sérénité",
        "Pas de poursuite ": "Pas de poursuite ",
        "Réalisation d'un audit énergétique": "Réalisation d'un audit énergétique",
        "Autre": "Autre"
      },
      "helptext": "",
      "mandatory": true,
      "multiple": true
    }
  ]
}
                    """,
                ),
                (
                    (menages_audit, copros_audit),
                    "Informations parcours SARE Ménages A3",
                    """
{
  "label": "Informations parcours SARE",
  "content": [
    {
      "id": "d_046",
      "type": "RadioButton",
      "label": "Visa conseiller",
      "choices": {
        "oui": "Oui",
        "non": "Non"
      },
      "helptext": "",
      "mandatory": false
    },
    {
      "id": "d_044b",
      "type": "RadioButton",
      "label": "Rapport d'Audit / DTG remis au demandeur",
      "choices": {
        "oui": "Oui",
        "non": "Non"
      },
      "helptext": "",
      "icon": "file-alt",
      "isAbstract": true,
      "mandatory": true
    }
  ]
}
                    """,
                ),
                (
                    (menages_accompagnement_real, copros_accompagnement_real),
                    "Informations parcours SARE Ménages A4",
                    """
{
  "label": "Informations parcours SARE",
  "content": [
    {
      "id": "d_047",
      "type": "DateField",
      "label": "Date de signature de l'engagement",
      "mandatory": true
    },
    {
      "id": "d_058",
      "type": "DateField",
      "label": "Date 1ère visite",
      "isAbstract": true,
      "icon": "eye",
      "helptext": "",
      "mandatory": false
    },
    {
      "id": "d_060",
      "type": "DateField",
      "label": "Date du 1er devis déposé",
      "isAbstract": true,
      "icon": "file-alt",
      "helptext": "",
      "mandatory": false
    },
    {
      "id": "d_049",
      "type": "DateField",
      "label": "Date de démarrage des travaux",
      "isAbstract": true,
      "icon": "calendar-check",
      "helptext": "",
      "mandatory": false
    },
    {
      "id": "d_052",
      "type": "RadioButton",
      "label": "Abandon de l’accompagnement",
      "choices": {
        "oui": "Oui",
        "non": "Non"
      },
      "helptext": "",
      "mandatory": true
    },
    {
      "id": "d_053",
      "type": "NumberField",
      "label": "Temps passé lors de l'accompagnement",
      "icon": ["fal", "hourglass-half"],
      "helptext": "",
      "mandatory": false
    }
  ]
}
                    """,
                ),
                (
                    (menages_accompagnement_suivi, copros_accompagnement_suivi),
                    "Informations parcours SARE Ménages A4bis",
                    """
{
  "label": "Informations parcours SARE",
  "content": [
    {
      "id": "d_047",
      "type": "DateField",
      "label": "Date de signature de l'engagement",
      "mandatory": true
    },
    {
      "id": "d_060",
      "type": "DateField",
      "label": "Date du 1er devis déposé",
      "mandatory": false
    },
    {
      "id": "d_049",
      "type": "DateField",
      "label": "Date de démarrage des travaux",
      "mandatory": false
    },
    {
      "id": "d_050",
      "type": "DateField",
      "label": "Date de bilan de fin de travaux",
      "mandatory": false
    },
    {
      "id": "d_052",
      "type": "RadioButton",
      "label": "Abandon de l’accompagnement",
      "choices": {
        "oui": "Oui",
        "non": "Non"
      },
      "helptext": "",
      "mandatory": true
    },
    {
      "id": "d_063",
      "type": "RadioButton",
      "label": "Bilan de consommation",
      "choices": {
        "oui": "Oui",
        "non": "Non"
      },
      "mandatory": true
    },
    {
      "id": "d_065",
      "type": "DateField",
      "label": "Date du test d'étanchéité à l'air",
      "mandatory": false
    },
    {
      "id": "d_067",
      "type": "DateField",
      "label": "Date de prise en main finale",
      "mandatory": false
    },
    {
      "id": "d_053",
      "type": "NumberField",
      "label": "Temps passé lors de l'accompagnement",
      "icon": ["fal", "hourglass-half"],
      "helptext": "",
      "mandatory": false
    }
  ]
}
                    """,
                ),
                (
                    (menages_moe, copros_moe),
                    "Informations parcours SARE Ménages A5",
                    """
{
  "label": "Informations parcours SARE",
  "content": [
    {
      "id": "d_047",
      "type": "DateField",
      "label": "Date de signature de l'engagement",
      "mandatory": true
    },
    {
      "id": "d_049",
      "type": "DateField",
      "label": "Date de démarrage des travaux",
      "mandatory": true
    },
    {
      "id": "d_050",
      "type": "DateField",
      "label": "Date de bilan de fin de travaux",
      "mandatory": true
    },
    {
      "id": "d_052",
      "type": "RadioButton",
      "label": "Abandon de l’accompagnement",
      "choices": {
        "oui": "Oui",
        "non": "Non"
      },
      "helptext": "",
      "mandatory": true
    },
    {
      "id": "d_053",
      "type": "NumberField",
      "label": "Temps passé lors de l'accompagnement",
      "icon": ["fal", "hourglass-half"],
      "helptext": "",
      "mandatory": false
    }
  ]
}
                    """,
                ),
                (
                    (tertiaire_infos, None),
                    "Informations parcours SARE petit tertiaire B1",
                    """
{
  "label": "Informations parcours SARE",
  "content": [
    {
      "id": "d_078",
      "type": "SelectList",
      "label": "Type d’information",
      "isAbstract": true,
      "icon": "info-circle",
      "choices": {
        "Information financière": "Information financière",
        "Information juridique": "Information juridique",
        "Information sociale": "Information sociale",
        "Information technique": "Information technique"
      },
      "helptext": "",
      "mandatory": true,
      "multiple": true
    },
    {
      "id": "d_079",
      "type": "SelectList",
      "label": "Nature de l’information",
      "isAbstract": true,
      "icon": "info-circle",
      "choices": {
         "Aides financières": "Aides financières",
         "Amélioration légère": "Amélioration légère",
         "Compréhension des factures d'énergie": "Compréhension des factures d'énergie",
         "Construction": "Construction",
         "Démarchage": "Démarchage",
         "Eco-gestes": "Eco-gestes",
         "Maintenance": "Maintenance",
         "Offres à 1€": "Offres à 1€",
         "Réglementation/Législation": "Réglementation/Législation",
         "Rénovation lourde": "Rénovation lourde",
         "Régulation": "Régulation"
      },
      "helptext": "",
      "multiple": true,
      "mandatory": false
    },
    {
      "id": "d_080",
      "type": "TextArea",
      "label": "Question",
      "helptext": "",
      "mandatory": true
    },
    {
      "id": "d_081",
      "type": "TextArea",
      "label": "Réponse",
      "helptext": "",
      "mandatory": true
    }
  ]
}
                    """,
                ),
                (
                    (tertiaire_conseil_perso, None),
                    "Informations parcours SARE petit tertiaire B2",
                    """
{
  "label": "Informations parcours SARE",
  "content": [
    {
      "id": "d_085",
      "type": "SelectList",
      "label": "Nature de l’information technique du conseil",
      "isAbstract": true,
      "icon": "arrow-alt-circle-right",
      "choices": {
        "Bâti": "Bâti",
        "Process": "Process",
        "Usages": "Usages"
      },
      "helptext": "",
      "mandatory": true,
      "multiple": true
    },
    {
      "id": "d_087",
      "type": "SelectList",
      "label": "Poursuite de service envisagée",
      "isAbstract": true,
      "icon": "arrow-alt-circle-right",
      "choices": {
        "Accompagnement complet entreprise (MOE/AMO)": "Accompagnement complet entreprise (MOE/AMO)",
        "Action bâti": "Action bâti",
        "Action process": "Action process",
        "Action usage": "Action usage",
        "Pas de poursuite ": "Pas de poursuite ",
        "Programme existant": "Programme existant",
        "Réalisation d'un audit énergétique": "Réalisation d'un audit énergétique",
        "Autre": "Autre"
      },
      "helptext": "",
      "mandatory": true,
      "multiple": true
    }
  ]
}
                    """,
                ),
            ]
        )

        print("Creating CustomForms : Contact")

        [sare_contacts_folder_model] = create_custom_forms_folder_models(
            [
                (
                    (menages,),
                    "Contact",
                    "Formulaire SARE / Ménages",
                    """
{
   "label":"Informations parcours SARE",
   "content":[
       {
      "type": "Row",
      "cells": [
        {
            "foundationClass": "small-12 medium-6",
            "children": [
                {
                   "id":"publicType",
                   "type":"SelectList",
                   "label":"Type de public",
                   "choices":{
                      "Locataire":"Locataire",
                      "Occupant à titre gratuit":"Occupant à titre gratuit",
                      "PB":"PB (Propriétaire Bailleur)",
                      "PO ou PB membre d’une SCI":"PO ou PB membre d’une SCI",
                      "PO":"PO (Propriétaire Occupant)",
                      "Professionnel":"Professionnel",
                      "Autre":"Autre"
                   },
                   "order": [
                      "Locataire",
                      "Occupant à titre gratuit",
                      "PB",
                      "PO ou PB membre d’une SCI",
                      "PO",
                      "Professionnel",
                      "Autre"
                   ],
                   "helptext":"",
                   "mandatory":true
                },
                {
                    "id":"d_012",
                    "type":"SelectList",
                    "label":"Eligibilité aux aides ANAH",
                    "choices":{
                        "Oui":"Oui",
                        "Non":"Non",
                        "NSP":"Ne sait pas"
                    },
                    "helptext":"",
                    "mandatory":true
                },
                {
                    "id": "revenuFiscalDeReference",
                    "type": "NumberField",
                    "label": "Revenu fiscal de référence",
                    "icon": "euro-sign",
                    "helptext": "",
                    "minValue": 0,
                    "mandatory":true
                },
                {
                    "id":"couleurMaPrimeRenov",
                    "type":"SelectList",
                    "label":"Couleur Ma Prime Rénov'",
                    "choices":{
                        "bleu": "Bleu",
                        "jaune": "Jaune",
                        "violet": "Violet",
                        "rose": "Rose"
                    },
                    "order": ["bleu", "jaune", "violet", "rose"],
                    "helptext":"",
                    "mandatory":false
                }
            ]
        },
        {
            "foundationClass": "small-12 medium-6",
            "children": [
                {
                    "id":"d_015",
                    "type":"SelectList",
                    "label":"Type de logement",
                    "choices":{
                        "Logement individuel":"Logement individuel",
                        "Logement en copropriété":"Logement en copropriété"
                    },
                    "helptext":"",
                    "mandatory":true,
                    "minChoices":1,
                    "maxChoices":1
                },
                {
                   "id":"houseConstructionYear",
                   "type":"NumberField",
                   "label":"Année de construction du logement",
                   "icon":[
                      "fal",
                      "house"
                   ],
                   "helptext":"",
                   "mandatory":false
                },
                {
                    "id": "nbPersonsInHousing",
                    "type": "NumberField",
                    "label": "Nombre de personnes dans le logement",
                    "icon": "users",
                    "helptext": "",
                    "mandatory": true
                }
            ]
        }
      ]
    }
   ]
}
                    """,
                ),
            ]
        )

        [sare_copro_contacts_folder_model] = create_custom_forms_folder_models(
            [
                (
                    (copros,),
                    "Contact",
                    "Formulaire SARE / Copro",
                    """
{
   "label":"Informations parcours SARE",
   "content":[
       {
      "type": "Row",
      "cells": [
        {
            "foundationClass": "small-12 medium-6",
            "children": [
                {
                   "id":"publicType",
                   "type":"SelectList",
                   "label":"Type de public",
                   "choices":{
                      "Locataire":"Locataire",
                      "Membre ou président de conseil syndical":"Membre ou président de conseil syndical",
                      "Occupant à titre gratuit":"Occupant à titre gratuit",
                      "PB":"PB (Propriétaire Bailleur)",
                      "PO ou PB membre d’une SCI":"PO ou PB membre d’une SCI",
                      "PO":"PO (Propriétaire Occupant)",
                      "Professionnel":"Professionnel",
                      "Autre":"Autre"
                   },
                   "order": [
                      "Locataire",
                      "Membre ou président de conseil syndical",
                      "Occupant à titre gratuit",
                      "PB",
                      "PO ou PB membre d’une SCI",
                      "PO",
                      "Professionnel",
                      "Autre"
                   ],
                   "helptext":"",
                   "mandatory":true
                },
                {
                    "id":"d_012",
                    "type":"SelectList",
                    "label":"Eligibilité aux aides ANAH",
                    "choices":{
                        "Oui":"Oui",
                        "Non":"Non",
                        "NSP":"Ne sait pas"
                    },
                    "helptext":"",
                    "mandatory":true
                },
                {
                    "id": "revenuFiscalDeReference",
                    "type": "NumberField",
                    "label": "Revenu fiscal de référence",
                    "icon": "euro-sign",
                    "helptext": "",
                    "minValue": 0,
                    "mandatory":true
                },
                {
                    "id":"couleurMaPrimeRenov",
                    "type":"SelectList",
                    "label":"Couleur Ma Prime Rénov'",
                    "choices":{
                        "bleu": "Bleu",
                        "jaune": "Jaune",
                        "violet": "Violet",
                        "rose": "Rose"
                    },
                    "order": ["bleu", "jaune", "violet", "rose"],
                    "helptext":"",
                    "mandatory":false
                }
            ]
        },
        {
            "foundationClass": "small-12 medium-6",
            "children": [
                {
                    "id":"d_015",
                    "type":"SelectList",
                    "label":"Type de logement",
                    "choices":{
                        "Logement en copropriété":"Logement en copropriété"
                    },
                    "default":"Logement en copropriété",
                    "helptext":"",
                    "mandatory":true,
                    "minChoices":1,
                    "maxChoices":1
                },
                {
                   "id":"houseConstructionYear",
                   "type":"NumberField",
                   "label":"Année de construction du logement",
                   "icon":[
                      "fal",
                      "house"
                   ],
                   "helptext":"",
                   "mandatory":false
                },
                {
                    "id": "nbPersonsInHousing",
                    "type": "NumberField",
                    "label": "Nombre de personnes dans le logement",
                    "icon": "users",
                    "helptext": "",
                    "mandatory": true
                },
                {
                    "id": "d_029",
                    "type": "NumberField",
                    "label": "Nombre de logements dans la copro",
                    "icon": ["far", "city"],
                    "helptext": "",
                    "mandatory": false
                }
            ]
        }
      ]
    }
   ]
}
                    """,
                ),
            ]
        )

        print("Creating CustomForms : Organization")

        [sare_organizations_folder_model] = create_custom_forms_folder_models(
            [
                (
                    (copros,),
                    "Organization",
                    "Formulaire SARE / Copro",
                    """
{
   "label":"Informations parcours SARE",
   "content":[
       {
      "type": "Row",
      "cells": [
        {
            "foundationClass": "small-12 medium-6",
            "children": [
                {
                   "id":"publicType",
                   "type":"SelectList",
                   "label":"Type de public",
                   "choices":{
                      "Membre ou président de conseil syndical":"Membre ou président de conseil syndical",
                      "SCI":"SCI",
                      "Syndic de copropriétés":"Syndic de copropriétés",
                      "Autre":"Autre"
                   },
                   "order": [
                      "Membre ou président de conseil syndical",
                      "SCI",
                      "Syndic de copropriétés",
                      "Autre"
                   ],
                   "helptext":"",
                   "mandatory":true
                },
                {
                    "id": "d_069",
                    "type": "TextField",
                    "label": "Numéro de SIRET",
                    "icon": "warehouse",
                    "helptext": "",
                    "mandatory": false
                },
                {
                    "id":"d_015",
                    "type":"SelectList",
                    "label":"Type de logement",
                    "choices":{
                        "Copropriété":"Copropriété"
                    },
                    "default":"Copropriété",
                    "helptext":"",
                    "mandatory":true,
                    "minChoices":1,
                    "maxChoices":1
                }
            ]
        },
        {
            "foundationClass": "small-12 medium-6",
            "children": [
                {
                   "id":"houseConstructionYear",
                   "type":"NumberField",
                   "label":"Année de construction du logement",
                   "icon":[
                      "fal",
                      "house"
                   ],
                   "helptext":"",
                   "mandatory":false
                },
                {
                    "id": "d_029",
                    "type": "NumberField",
                    "label": "Nombre de logements dans la copro",
                    "icon": ["far", "city"],
                    "helptext": "",
                    "mandatory": true
                }
            ]
        }
      ]
    }
   ]
}
                    """,
                ),
            ]
        )

        return


def map_first(list_of_tuples):
    return [first for first, _ in list_of_tuples]


def create_custom_forms_actions(custom_forms):
    def new_custom_form(action_model, name, form):
        if action_model is None:
            return

        obj, created = CustomForm.objects.get_or_create(
            model="Action",
            anchor="Informations",
            description=name,
            defaults={
                "version": 0,
                "form": json.loads(form),
            },
        )
        print("---", action_model)
        if not created:
            obj.form = json.loads(form)
            obj.save()
            print("---- updated")

        obj.action_models.add(action_model)
        return obj

    return map_first(
        [
            [
                new_custom_form(action_model, name, form)
                for action_model in action_models
            ]
            for order, (action_models, name, form) in enumerate(custom_forms)
        ]
    )


def create_custom_forms_for_project_on_contact(project):
    obj = CustomForm.objects.filter(
        model="Contact",
        anchor="Identity",
        description="Complement de formulaire pour SARE",
    )
    if obj.exists():
        obj.delete()
        print("---- deleted")

    return obj


def create_custom_forms_for_folder_on_organization(folder):
    form = """
{
  "label": "Information parcours petit tertiaire",
  "content": [
       {
      "type": "Row",
      "cells": [
        {
            "foundationClass": "small-12 medium-6",
            "children": [
    {
      "id": "d_069",
      "type": "TextField",
      "label": "Numéro de SIRET",
      "icon": "warehouse",
      "helptext": "",
      "mandatory": true
    }
]
},

        {
            "foundationClass": "small-12 medium-6",
            "children": [

    {
      "id": "d_074",
      "type": "SelectList",
      "label": "Statut d'occupation",
      "icon": "arrow-alt-circle-right",
      "choices": {
         "Locataire": "Locataire",
         "Propriétaire": "Propriétaire"
      },
      "helptext": "",
      "mandatory": true,
      "multiple": false
    }
]
}
  ]
}
]
}
    """
    obj, created = CustomForm.objects.get_or_create(
        model="Organization",
        anchor="Informations",
        description="Information parcours petit tertiaire",
        defaults={
            "version": 0,
            "form": json.loads(form),
        },
    )
    if not created:
        obj.form = json.loads(form)
        obj.save()
        print("---- updated")

    obj.folder_models.add(folder)
    return obj


def create_custom_forms_folder_models(custom_forms):
    def new_custom_form(model, folder_model, name, form):
        obj, created = CustomForm.objects.get_or_create(
            model=model,
            anchor="Informations",
            description=name,
            defaults={
                "version": 0,
                "form": json.loads(form),
            },
        )
        print("---", folder_model)
        if not created:
            obj.form = json.loads(form)
            obj.save()
            print("---- updated")

        obj.folder_models.add(folder_model)
        return obj

    return [
        [
            new_custom_form(model, folder_model, name, form)
            for folder_model in folder_models
        ]
        for order, (folder_models, model, name, form) in enumerate(custom_forms)
    ]


def create_status(folder_model, names):
    return map_first(
        [
            Status.objects.get_or_create(
                name=name, folder_model=folder_model, defaults={"order": order}
            )
            for order, name in enumerate(names)
        ]
    )


def create_category_models(folder_model, names):
    return map_first(
        [
            CategoryModel.objects.get_or_create(
                name=name, folder_model=folder_model, defaults={"order": order}
            )
            for order, name in enumerate(names)
        ]
    )


def create_action_models(actions):
    return map_first(
        [
            ActionModel.objects.update_or_create(
                name=name,
                category_model=category,
                defaults={
                    "description": description,
                    "order": order,
                    "trigger_status": trigger_status,
                    "default": action_type is ActionType.ONE
                    or action_type is ActionType.ONE_OR_MORE,
                    "optional": action_type is ActionType.ZERO_OR_MORE
                    or action_type is ActionType.ONE_OR_MORE,
                    "coefficient_enabled": ActionBooleans.COEFFICIENT_ENABLED
                    in booleans,
                    "message_required": ActionBooleans.MESSAGE_REQUIRED in booleans,
                    "file_required": ActionBooleans.FILE_REQUIRED in booleans,
                    "contact_required": ActionBooleans.CONTACT_REQUIRED in booleans,
                },
            )
            for order, (
                category,
                name,
                description,
                action_type,
                trigger_status,
                booleans,
            ) in enumerate(actions)
        ]
    )

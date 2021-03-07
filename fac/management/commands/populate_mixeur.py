"""
Ce script permet de générer un modèle de dossier de suivi client Mixeur.

Pour le lancer :

    inv run -c "populate_mixeur"

S'il rencontre un problème à l'exécution, rien ne sera créé.

Pour supprimer tout ce qui a été créé : supprimer le projet Mixeur
"""

import datetime
from enum import Enum, auto

from django.db import transaction
from django.core.management.base import BaseCommand

from fac.models import (
    FolderModel,
    ActionModel,
    CategoryModel,
    Project,
    Status,
    TypeValorization,
    Valorization,
    Period,
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
    help = "Create models for Mixeur project"

    @transaction.atomic
    def handle(self, *args, **options):
        project, _ = Project.objects.get_or_create(name="Mixeur")

        print("Creating Folder models…")
        mixeur_project, _ = map_first(
            [
                FolderModel.objects.get_or_create(
                    name=name, defaults={"icon": icon, "project": project}
                )
                for name, icon in [("Suivi CU", "blender"), ("prout", "blender")]
            ]
        )

        ##########
        # Mixeur #
        ##########

        print(f"Filling folder model :")
        [mixeur_prospect, mixeur_en_cours, mixeur_membre,] = create_status(
            mixeur_project,
            [
                "Prospect",
                "En cours d'adhésion",
                "Membre",
            ],
        )

        [
            mixeur_prospection,
            mixeur_contractualisation,
            mixeur_deploiement,
            mixeur_presta,
        ] = create_category_models(
            mixeur_project,
            [
                "Prospection",
                "Contractualisation",
                "Déploiement",
                "Prestations complémentaires",
            ],
        )

        [
            mixeur_rdv_echange_prospect,
            mixeur_presentation,
            mixeur_demo,
            mixeur_rdv_echange_contrat,
            mixeur_conv_envoyee,
            mixeur_conv_recue,
            mixeur_devis_envoye,
            mixeur_devis_retourne,
            mixeur_facture,
            mixeur_renouvellement,
            mixeur_offre_envoyee,
            mixeur_offre_recue,
            mixeur_offre_devis_envoye,
            mixeur_offre_devis_recu,
            mixeur_offre_facture_envoyee,
            mixeur_import,
            mixeur_mb,
            mixeur_formation,
            mixeur_parcours_perso,
            mixeur_presta_devis_envoye,
            mixeur_presta_devis_retourne,
            mixeur_presta_facture,
        ] = create_action_models(
            [
                (
                    mixeur_prospection,
                    "RDV/Echange",
                    """""",
                    ActionType.ZERO_OR_MORE,
                    None,
                    (),
                ),
                (
                    mixeur_prospection,
                    "Présentation ou démo",
                    """""",
                    ActionType.ONE_OR_MORE,
                    None,
                    (),
                ),
                (
                    mixeur_prospection,
                    "Accès démo",
                    """Noter les codes d'accès du prospect et activer un rappel pour la fin de validité de la démo.""",
                    ActionType.ONE_OR_MORE,
                    None,
                    (),
                ),
                (
                    mixeur_contractualisation,
                    "RDV/Echange",
                    """""",
                    ActionType.ZERO_OR_MORE,
                    None,
                    (),
                ),
                (
                    mixeur_contractualisation,
                    "Convention envoyée",
                    """""",
                    ActionType.ONE,
                    mixeur_en_cours,
                    (),
                ),
                (
                    mixeur_contractualisation,
                    "Convention reçue signée",
                    """""",
                    ActionType.ONE,
                    mixeur_en_cours,
                    (),
                ),
                (
                    mixeur_contractualisation,
                    "Devis envoyé",
                    """""",
                    ActionType.ONE_OR_MORE,
                    None,
                    (),
                ),
                (
                    mixeur_contractualisation,
                    "Devis retourné signé",
                    """""",
                    ActionType.ONE_OR_MORE,
                    mixeur_membre,
                    (),
                ),
                (
                    mixeur_contractualisation,
                    "Facture envoyée",
                    """""",
                    ActionType.ONE_OR_MORE,
                    None,
                    (),
                ),
                (
                    mixeur_contractualisation,
                    "Renouvellement adhésion",
                    """""",
                    ActionType.ZERO_OR_MORE,
                    None,
                    (),
                ),
                (
                    mixeur_deploiement,
                    "Offre de déploiement envoyée",
                    """""",
                    ActionType.ONE,
                    mixeur_en_cours,
                    (),
                ),
                (
                    mixeur_deploiement,
                    "Offre de déploiement reçue signée",
                    """""",
                    ActionType.ONE,
                    mixeur_en_cours,
                    (),
                ),
                (
                    mixeur_deploiement,
                    "Devis envoyé",
                    """""",
                    ActionType.ONE,
                    None,
                    (),
                ),
                (
                    mixeur_deploiement,
                    "Devis retourné signé",
                    """""",
                    ActionType.ONE,
                    mixeur_membre,
                    (),
                ),
                (
                    mixeur_contractualisation,
                    "Facture envoyée",
                    """""",
                    ActionType.ONE,
                    None,
                    (),
                ),
                (
                    mixeur_deploiement,
                    "Import de données",
                    """""",
                    ActionType.ZERO_OR_MORE,
                    None,
                    (),
                ),
                (
                    mixeur_deploiement,
                    "Personnalisation instance",
                    """""",
                    ActionType.ZERO_OR_MORE,
                    None,
                    (),
                ),
                (
                    mixeur_presta,
                    "Formation spécifique",
                    """""",
                    ActionType.ZERO_OR_MORE,
                    None,
                    (),
                ),
                (
                    mixeur_presta,
                    "Parcours personnalisé",
                    """""",
                    ActionType.ZERO_OR_MORE,
                    None,
                    (),
                ),
                (
                    mixeur_presta,
                    "Devis envoyé",
                    """""",
                    ActionType.ONE_OR_MORE,
                    None,
                    (),
                ),
                (
                    mixeur_presta,
                    "Devis retourné signé",
                    """""",
                    ActionType.ONE_OR_MORE,
                    mixeur_membre,
                    (),
                ),
                (
                    mixeur_presta,
                    "Facture envoyée",
                    """""",
                    ActionType.ONE_OR_MORE,
                    None,
                    (),
                ),
            ]
        )


def map_first(list_of_tuples):
    return [first for first, _ in list_of_tuples]


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

"""
Ce script permet de générer tous les modèles de dossiers, actions, etc, pour
le projet de Démo (suivi d'une relation commerciale).

Pour le lancer :

    inv run -c "populate_demo_facp"

S'il rencontre un problème à l'exécution, rien ne sera créé.

Pour supprimer tout ce qui a été créé : supprimer le projet Démo, ainsi que
les deux types de valorisation.
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
    help = "Create models for Demo project"

    @transaction.atomic
    def handle(self, *args, **options):
        project, _ = Project.objects.get_or_create(name="Demo")

        print("Creating Folder models…")
        clients, associations = map_first(
            [
                FolderModel.objects.get_or_create(
                    name=name, defaults={"icon": icon, "project": project}
                )
                for name, icon in [
                    ("Suivi relation client", "user-tie"),
                    ("Suivi relation client d'intérêt général", "hands-helping"),
                ]
            ]
        )

        print("Creating valorization types…")
        metropole, domtom = map_first(
            [
                TypeValorization.objects.get_or_create(name=name)
                for name in ["Métropole", "DOM-TOM"]
            ]
        )
        project.type_valorizations.add(metropole, domtom)

        year_period, _ = Period.objects.update_or_create(
            name="Année 2020",
            defaults={
                "date_start": datetime.date(year=2020, month=1, day=1),
                "date_end": datetime.date(year=2020, month=12, day=31),
            },
        )

        #########################
        # Suivi relation client #
        #########################

        print(f"Filling folder model : {clients.name}")
        [
            clients_prospect,
            clients_devis_envoye,
            clients_devis_signe,
            clients_client,
        ] = create_status(
            clients, ["Prospect", "Devis envoyé", "Devis signé", "Client"]
        )

        [
            clients_prospection,
            clients_suivi,
            clients_maintenance,
        ] = create_category_models(clients, ["Prospection", "Suivi", "Maintenance"])

        [
            clients_demarchage,
            clients_demo,
            clients_info,
            clients_rdv,
            clients_echange,
            clients_commande,
            clients_formation,
            clients_bilan,
            clients_sav,
            clients_intervention,
        ] = create_action_models(
            [
                (
                    clients_prospection,
                    "Démarchage téléphonique",
                    "",
                    ActionType.ONE,
                    clients_prospect,
                    (),
                ),
                (clients_prospection, "Démo", "", ActionType.ONE, clients_prospect, ()),
                (
                    clients_prospection,
                    "Demande d'information",
                    """Demande d'information préalables à la commande.""",
                    ActionType.ONE_OR_MORE,
                    None,
                    (),
                ),
                (
                    clients_suivi,
                    "Rendez-vous",
                    """Merci de renseigner la personne rencontrée au sein de la structure concernée en remplissant le
                    champ “contact associé”.""",
                    ActionType.ONE_OR_MORE,
                    None,
                    (ActionBooleans.CONTACT_REQUIRED,),
                ),
                (
                    clients_suivi,
                    "Echange",
                    """Echange téléphonique ou mail.""",
                    ActionType.ONE_OR_MORE,
                    None,
                    (),
                ),
                (
                    clients_suivi,
                    "Commande passée",
                    """Merci de joindre le devis et le bon de commande signés.""",
                    ActionType.ONE_OR_MORE,
                    clients_client,
                    (ActionBooleans.FILE_REQUIRED,),
                ),
                (
                    clients_suivi,
                    "Formation",
                    """Merci de renseigner la personne rencontrée au sein de la structure concernée en remplissant le
                    champ “contact associé”.""",
                    ActionType.ONE_OR_MORE,
                    None,
                    (ActionBooleans.CONTACT_REQUIRED,),
                ),
                (
                    clients_suivi,
                    "Bilan",
                    """Echange téléphonique ou mail.""",
                    ActionType.ONE_OR_MORE,
                    None,
                    (),
                ),
                (
                    clients_maintenance,
                    "Demande SAV",
                    "",
                    ActionType.ONE_OR_MORE,
                    None,
                    (),
                ),
                (
                    clients_maintenance,
                    "Intervention",
                    "",
                    ActionType.ONE_OR_MORE,
                    None,
                    (ActionBooleans.FILE_REQUIRED,),
                ),
            ]
        )

        for actions, valorizations in [
            (
                [clients_demarchage, clients_info, clients_echange, clients_sav],
                [(metropole, 51), (domtom, 46)],
            ),
            (
                [
                    clients_demo,
                    clients_rdv,
                    clients_formation,
                    clients_bilan,
                    clients_intervention,
                ],
                [(metropole, 780), (domtom, 765)],
            ),
            ([clients_commande], [(metropole, 1500), (domtom, 1485)]),
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
                                    "period": year_period,
                                },
                            )
                            for type_valorization, amount in valorizations
                        ]
                    )
                )

        return


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

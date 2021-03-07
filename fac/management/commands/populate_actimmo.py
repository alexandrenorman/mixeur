"""
Ce script permet de générer tous les modèles de dossiers, actions, etc, pour
Actimmo.

Pour le lancer :

    inv run -c "populate_actimmo"

S'il rencontre un problème à l'exécution, rien ne sera créé.

Pour supprimer tout ce qui a été créé : supprimer le projet Actimmo, ainsi que
les trois types de valorisation.
"""

import datetime
from enum import Enum, auto

from django.core.management.base import BaseCommand
from django.db import transaction
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
    help = "Create models for Actimmo organizations"

    @transaction.atomic
    def handle(self, *args, **options):
        project, _ = Project.objects.get_or_create(name="Actimmo")

        print("Creating Folder models…")
        banque, agence, chambre, office = map_first(
            [
                FolderModel.objects.get_or_create(
                    name=name, defaults={"icon": icon, "project": project}
                )
                for name, icon in [
                    ("Banque", "euro-sign"),
                    ("Agence immobilière", "house"),
                    ("Chambre départementale des notaires", "file-alt"),
                    ("Office notarial", "pen-fancy"),
                ]
            ]
        )

        print("Creating valorization types…")
        rural, urbain, mixte = map_first(
            [
                TypeValorization.objects.get_or_create(name=name)
                for name in ["Rural", "Urbain", "Mixte"]
            ]
        )
        project.type_valorizations.add(rural, urbain, mixte)

        actimmo_period, _ = Period.objects.update_or_create(
            name="Période ACTIMMO",
            defaults={
                "date_start": datetime.date(year=2019, month=10, day=18),
                "date_end": datetime.date(year=2021, month=4, day=30),
            },
        )

        ##########
        # Banque #
        ##########

        print(f"Filling folder model : {banque.name}")
        [
            banque_a_contacter,
            banque_demarchee,
            banque_rencontree,
            banque_formee,
            banque_partenaire,
        ] = create_status(
            banque,
            [
                "Structure à contacter",
                "Structure démarchée",
                "Structure rencontrée",
                "Structure formée",
                "Structure partenaire",
            ],
        )

        [
            banque_demarchage,
            banque_rdv_approfondi,
            banque_formation,
            banque_partenariat,
        ] = create_category_models(
            banque,
            [
                "Démarchage",
                "Rendez-vous approfondi",
                "Formation",
                "Formalisation du partenariat",
            ],
        )

        [
            banque_porte_a_porte,
            banque_rdv,
            banque_reunion,
            banque_prep_charte,
            banque_signature_charte,
        ] = create_action_models(
            [
                (
                    banque_demarchage,
                    "Porte-à-porte",
                    """Cette action correspond à un démarchage physique au sein de la structure.
                    Action forfaitisée, 1 seul forfait déclenchable par structure.""",
                    ActionType.ONE,
                    banque_demarchee,
                    (),
                ),
                (
                    banque_rdv_approfondi,
                    "Rendez-vous",
                    """Merci de renseigner la personne rencontrée au sein de la structure concernée en remplissant le
                    champ “contact associé”.
                    Action forfaitisée, 1 forfait par action réalisée.""",
                    ActionType.ONE_OR_MORE,
                    banque_rencontree,
                    (ActionBooleans.CONTACT_REQUIRED,),
                ),
                (
                    banque_formation,
                    "Réunion d’équipe/formation",
                    """Merci de préciser le format de la formation (intervention en réunion d’équipe, formation, etc.),
                    la durée approximative, le nombre de participants et leur poste dans la structure (conseillers,
                    directeurs d’agence, etc.) en renseignant le champ “Commentaires”.
                    Action forfaitisée, 1 forfait par action réalisée.""",
                    ActionType.ONE_OR_MORE,
                    banque_formee,
                    (ActionBooleans.MESSAGE_REQUIRED,),
                ),
                (
                    banque_partenariat,
                    "Préparation de la charte",
                    """Action non forfaitisée.""",
                    ActionType.ONE,
                    None,
                    (),
                ),
                (
                    banque_partenariat,
                    "Signature d'une charte",
                    """Merci de joindre la charte de partenariat signée par les parties concernées en pièce jointe.
                    Action forfaitisée, 1 seul forfait déclenchable par structure.""",
                    ActionType.ONE,
                    banque_partenaire,
                    (ActionBooleans.FILE_REQUIRED,),
                ),
            ]
        )

        ##########
        # Agence #
        ##########

        print(f"Filling folder model : {agence.name}")
        [
            agence_a_contacter,
            agence_demarchee,
            agence_rencontree,
            agence_formee,
            agence_partenaire,
        ] = create_status(
            agence,
            [
                "Structure à contacter",
                "Structure démarchée",
                "Structure rencontrée",
                "Structure formée",
                "Structure partenaire",
            ],
        )

        [
            agence_demarchage,
            agence_rdv_approfondi,
            agence_formation,
            agence_partenariat,
        ] = create_category_models(
            agence,
            [
                "Démarchage",
                "Rendez-vous approfondi",
                "Formation",
                "Formalisation du partenariat",
            ],
        )

        [
            agence_porte_a_porte,
            agence_rdv,
            agence_reunion,
            agence_prep_charte,
            agence_signature_charte,
            agence_preco_immo,
        ] = create_action_models(
            [
                (
                    agence_demarchage,
                    "Porte-à-porte",
                    """Cette action correspond à un démarchage physique au sein de la structure.
                    Action forfaitisée, 1 seul forfait déclenchable par structure.""",
                    ActionType.ONE,
                    agence_demarchee,
                    (),
                ),
                (
                    agence_rdv_approfondi,
                    "Rendez-vous",
                    """Merci de renseigner la personne rencontrée au sein de la structure concernée en remplissant le
                    champ “contact associé”.
                    Action forfaitisée, 1 forfait par action réalisée.""",
                    ActionType.ONE_OR_MORE,
                    agence_rencontree,
                    (ActionBooleans.CONTACT_REQUIRED,),
                ),
                (
                    agence_formation,
                    "Réunion d’équipe/formation",
                    """Merci de préciser le format de la formation (intervention en réunion d’équipe, formation, etc.),
                    la durée approximative, le nombre de participants et leur poste dans la structure (conseillers,
                    directeurs d’agence, etc.) en renseignant le champ “Commentaires”.
                    Action forfaitisée, 1 forfait par action réalisée.""",
                    ActionType.ONE_OR_MORE,
                    agence_formee,
                    (ActionBooleans.MESSAGE_REQUIRED,),
                ),
                (
                    agence_partenariat,
                    "Préparation de la charte",
                    """Action non forfaitisée.""",
                    ActionType.ONE,
                    None,
                    (),
                ),
                (
                    agence_partenariat,
                    "Signature d'une charte",
                    """Merci de joindre la charte de partenariat signée par les parties concernées en pièce jointe.
                    Action forfaitisée, 1 seul forfait déclenchable par structure.""",
                    ActionType.ONE,
                    agence_partenaire,
                    (ActionBooleans.FILE_REQUIRED,),
                ),
                (
                    agence_partenariat,
                    "Préco’immo",
                    """Merci de joindre le rapport correspondant en pièce jointe.
                    Action forfaitisée, 1 forfait par action réalisée.""",
                    ActionType.ONE_OR_MORE,
                    agence_partenaire,
                    (ActionBooleans.FILE_REQUIRED,),
                ),
            ]
        )

        ########################
        # Chambre des notaires #
        ########################

        print(f"Filling folder model : {chambre.name}")
        [
            chambre_a_contacter,
            chambre_rencontree,
            chambre_formee,
            chambre_partenaire,
        ] = create_status(
            chambre,
            [
                "Structure à contacter",
                "Structure rencontrée",
                "Structure partenaire",
                "Structure formée",
            ],
        )

        [
            chambre_amont,
            chambre_suivi_partenariat,
            chambre_autres,
        ] = create_category_models(
            chambre,
            [
                "Travail amont du partenariat",
                "Signature et suivi du partenariat",
                "Autres actions",
            ],
        )

        [
            chambre_demarchage,
            chambre_prep_charte,
            chambre_rdv_amont,
            chambre_signature_charte,
            chambre_rdv_partenaire,
            chambre_redaction_article,
            chambre_evenement,
            chambre_intervention,
        ] = create_action_models(
            [
                (
                    chambre_amont,
                    "Prise de contact/démarchage",
                    """Cette action déclenche le forfait “Travail amont partenariat chambre des notaires / notaires” qui
                    englobe l'ensemble des actions de l'étape "Travail amont partenariat" du parcours Chambre
                    départementale des notaires et de l'étape  "Démarchage et réunions approfondies" du parcours Office
                    notarial.
                    1 seul forfait déclenchable par lauréat.""",
                    ActionType.ONE,
                    chambre_rencontree,
                    (ActionBooleans.COEFFICIENT_ENABLED,),
                ),
                (
                    chambre_amont,
                    "Préparation de la charte",
                    """Action inclue dans le forfait “Travail amont partenariat chambre des notaires / notaires”
                    déclenché par l’action “Prise de contact/démarchage”.""",
                    ActionType.ZERO_OR_MORE,
                    chambre_rencontree,
                    (),
                ),
                (
                    chambre_amont,
                    "Rendez-vous/réunion",
                    """Merci de renseigner la personne rencontrée au sein de la structure concernée en remplissant le
                    champ “contact associé”.
                    Action inclue dans le forfait “Travail amont partenariat chambre des notaires / notaires” déclenché
                    par l’action “Prise de contact/démarchage”.""",
                    ActionType.ZERO_OR_MORE,
                    None,
                    (ActionBooleans.CONTACT_REQUIRED,),
                ),
                (
                    chambre_suivi_partenariat,
                    "Signature d'une charte",
                    """Merci de joindre la charte de partenariat signée par les parties concernées en pièce jointe.
                    Cette action déclenche le forfait “Signature et suivi partenariat chambre des notaires” qui englobe
                    l'ensemble des actions de l'étape "Signature et suivi du partenariat" du parcours Chambre
                    départementale des notaires.
                    1 seul forfait déclenchable par lauréat.""",
                    ActionType.ONE,
                    chambre_partenaire,
                    (ActionBooleans.FILE_REQUIRED, ActionBooleans.COEFFICIENT_ENABLED),
                ),
                (
                    chambre_suivi_partenariat,
                    "Rendez-vous/réunion",
                    """Merci de renseigner la personne rencontrée au sein de la structure concernée en remplissant le
                    champ “contact associé”.
                    Action inclue dans le forfait “Signature et suivi partenariat chambre des notaires” déclenché par
                    l’action “Signature d’une charte”.""",
                    ActionType.ZERO_OR_MORE,
                    None,
                    (ActionBooleans.CONTACT_REQUIRED,),
                ),
                (
                    chambre_autres,
                    "Rédaction communication article",
                    """Merci de joindre l’article publié en pièce jointe.
                    Action forfaitisée, 1 forfait par action réalisée.""",
                    ActionType.ZERO_OR_MORE,
                    None,
                    (ActionBooleans.FILE_REQUIRED,),
                ),
                (
                    chambre_autres,
                    "Participation à un événement",
                    """Merci de préciser le nom et la nature de l'événement (en lien avec la Chambre départementale des
                    notaires), le nombre de participants et en quoi a consisté votre participation en renseignant le
                    champ “Commentaires”.
                    Action forfaitisée, 1 forfait par action réalisée.""",
                    ActionType.ZERO_OR_MORE,
                    None,
                    (ActionBooleans.MESSAGE_REQUIRED,),
                ),
                (
                    chambre_autres,
                    "Intervention/formation",
                    """Merci de préciser le format de la formation (intervention en réunion d’équipe, formation, etc.),
                    la durée approximative, le nombre de participants et leur poste dans la structure en renseignant le
                    champ “Commentaires”.
                    Action forfaitisée, 1 forfait par action réalisée.""",
                    ActionType.ZERO_OR_MORE,
                    chambre_formee,
                    (ActionBooleans.MESSAGE_REQUIRED,),
                ),
            ]
        )

        ####################
        # Office notariaux #
        ####################

        print(f"Filling folder model : {office.name}")
        [office_a_contacter, office_rencontree, office_formee] = create_status(
            office,
            ["Structure à contacter", "Structure rencontrée", "Structure formée"],
        )

        [office_demarchage_et_rdv, office_autres] = create_category_models(
            office, ["Démarchage et rendez-vous approfondi", "Autres actions"]
        )

        [
            office_demarchage,
            office_rdv,
            office_redaction_article,
            office_intervention,
            office_preco_immo,
        ] = create_action_models(
            [
                (
                    office_demarchage_et_rdv,
                    "Prise de contact/démarchage",
                    """Action inclue dans le forfait “Travail amont partenariat chambre des notaires / notaires”
                    déclenché par l’action “Prise de contact/démarchage” du parcours Chambre départemental des
                    notaires.""",
                    ActionType.ONE,
                    office_rencontree,
                    (),
                ),
                (
                    office_demarchage_et_rdv,
                    "Rendez-vous/réunion",
                    """Merci de renseigner la personne rencontrée au sein de la structure concernée en remplissant le
                    champ “contact associé”.
                    Action inclue dans le forfait “Travail amont partenariat chambre des notaires / notaires” déclenché
                    par l’action “Prise de contact/démarchage” du parcours Chambre départemental des notaires.""",
                    ActionType.ZERO_OR_MORE,
                    None,
                    (ActionBooleans.CONTACT_REQUIRED,),
                ),
                (
                    office_autres,
                    "Rédaction communication article",
                    """Merci de joindre l’article publié en pièce jointe.
                    Action forfaitisée, 1 forfait par action réalisée.""",
                    ActionType.ZERO_OR_MORE,
                    None,
                    (ActionBooleans.FILE_REQUIRED,),
                ),
                (
                    office_autres,
                    "Intervention/formation",
                    """Merci de préciser le format de la formation (intervention en réunion d’équipe, formation, etc.),
                    la durée approximative, le nombre de participants et leur poste dans la structure en renseignant le
                    champ “Commentaires”.
                    Action forfaitisée, 1 forfait par action réalisée.""",
                    ActionType.ZERO_OR_MORE,
                    office_formee,
                    (ActionBooleans.MESSAGE_REQUIRED,),
                ),
                (
                    office_autres,
                    "Préco’immo",
                    """Merci de joindre le rapport correspondant en pièce jointe.
                    Action forfaitisée, 1 forfait par action réalisée.""",
                    ActionType.ONE_OR_MORE,
                    None,
                    (ActionBooleans.FILE_REQUIRED,),
                ),
            ]
        )

        for actions, valorizations in [
            (
                [banque_porte_a_porte, agence_porte_a_porte],
                [(rural, 51), (mixte, 46), (urbain, 41)],
            ),
            ([banque_rdv, agence_rdv], [(rural, 300), (mixte, 285), (urbain, 270)]),
            (
                [banque_reunion, agence_reunion],
                [(rural, 780), (mixte, 765), (urbain, 750)],
            ),
            (
                [banque_signature_charte, agence_signature_charte],
                [(rural, 1500), (mixte, 1485), (urbain, 1470)],
            ),
            (
                [agence_preco_immo, office_preco_immo],
                [(rural, 660), (mixte, 645), (urbain, 630)],
            ),
            (
                [chambre_demarchage, chambre_signature_charte],
                [(rural, 3660), (mixte, 3645), (urbain, 3630)],
            ),
            (
                [
                    chambre_redaction_article,
                    chambre_evenement,
                    chambre_intervention,
                    office_redaction_article,
                    office_intervention,
                ],
                [(rural, 1260), (mixte, 1245), (urbain, 1230)],
            ),
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
                                    "period": actimmo_period,
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

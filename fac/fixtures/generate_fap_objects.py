"""
Ce fichier permet de générer des fixtures pour la partie Fabrique à Projets de mixeur.
Il crée trois modèles de dossier avec ses sous objets :

    - Un modèle de dossier avec des objectifs et un budget.
    - Un modèle de dossier avec des objectifs et sans budget.
    - Un modèle de dossier sans objectif ni bugdet et donc sans période associée.

Au préalable, il faut restaurer la base de données de manière à n'avoir aucune donnée.

Puis lancer le script :

    # Lancement du shell Django dans un container existant
    $ inv django.run -c "shell"

    # Executer le script
    $ exec(open('fac/fixtures/generate_fap_objects.py').read())


À cette étape, toutes les données sont présentes en base de données.

Vous devez maintenant exporter ces données sous forme de fixtures :

    # Adapter en fonction des évolutions du modèle de données
    $ inv django.run -c "dumpdata accounts.group fac.project fac.typevalorization \
      fac.budget fac.period fac.valorization fac.foldermodel fac.status \
      fac.categorymodel fac.actionmodel fac.folder fac.contact fac.contact \
      fac.objectivestatus fac.objectiveaction fac.action --indent 2 --natural-foreign" \
      > /tmp/fixtures.json


S'assurer que /tmp/fixtures.json contient bien les données attendues, en restaurant à
nouveau la base et en réimportant directement les fixtures.
Enfin, copier /tmp/fixtures.json vers /fac/fixtures/fap_data_full.json

    $ mv /tmp/fixtures.json django/fac/fixtures/fap_data_full.json

"""


import random
from datetime import date, timedelta
from decimal import Decimal

from django.contrib.contenttypes.models import ContentType

from accounts.models import Group, User
from fac.models import (
    Project,
    TypeValorization,
    Budget,
    Period,
    Valorization,
    FolderModel,
    Status,
    CategoryModel,
    ActionModel,
    Folder,
    Contact,
    ObjectiveAction,
    ObjectiveStatus,
    Action,
    Organization,
)

# common
random.seed(78964537)
marie = Contact.objects.first()
orga = Organization.objects.first()
jean_conseiller = User.objects.get(pk=3)
pilot_group = Group.objects.get(pk=1)
assert marie and pilot_group
period = None
laureate_group1 = None
laureate_group2 = None


def create_commons():
    global period, laureate_group1, laureate_group2
    period = Period.objects.create(
        name="2020",
        date_start=date(year=2020, month=1, day=1),
        date_end=date(year=2020, month=12, day=31),
    )
    laureate_group1 = Group.objects.create(name="Lauréat1", coefficient=Decimal("0.7"))
    laureate_group2 = Group.objects.create(name="Lauréat2")
    laureate_group1.pilot_groups.add(pilot_group)
    laureate_group2.pilot_groups.add(pilot_group)


def generate_entries_valorizations():  # noqa: C901
    ville = TypeValorization.objects.create(name="ville")
    campagne = TypeValorization.objects.create(name="campagne")
    ville.groups.add(laureate_group1)
    campagne.groups.add(laureate_group2)

    # project with all things (valorization, budget objectives...)
    project1 = Project.objects.create(name="projet avec valorisations")
    project1.type_valorizations.add(ville)
    project1.type_valorizations.add(campagne)
    project1.groups.add(laureate_group1)
    project1.groups.add(laureate_group2)
    Budget.objects.create(
        period=period, total_envelope=30000, group=laureate_group1, project=project1
    )
    Budget.objects.create(
        period=period, total_envelope=30000, group=laureate_group2, project=project1
    )
    valorization_horaire1_ville = Valorization.objects.create(
        title="Valorisation horaire 1",
        act=False,
        amount=60.5,
        type_valorization=ville,
        period=period,
    )
    valorization_horaire2_ville = Valorization.objects.create(
        title="Valorisation horaire 2",
        act=False,
        amount=45.7,
        type_valorization=ville,
        period=period,
    )
    valorization_act1_ville = Valorization.objects.create(
        title="Valorisation acte 1",
        act=True,
        amount=53.4,
        type_valorization=ville,
        period=period,
    )
    valorization_act2_ville = Valorization.objects.create(
        title="Valorisation acte 2",
        act=True,
        amount=77.3,
        type_valorization=ville,
        period=period,
    )
    valorization_horaire1_campagne = Valorization.objects.create(
        title="Valorisation horaire 1",
        act=False,
        amount=50.5,
        type_valorization=campagne,
        period=period,
    )
    valorization_horaire2_campagne = Valorization.objects.create(
        title="Valorisation horaire 2",
        act=False,
        amount=35.7,
        type_valorization=campagne,
        period=period,
    )
    valorization_act1_campagne = Valorization.objects.create(
        title="Valorisation acte 1",
        act=True,
        amount=43.4,
        type_valorization=campagne,
        period=period,
    )
    valorization_act2_campagne = Valorization.objects.create(
        title="Valorisation acte 2",
        act=True,
        amount=67.3,
        type_valorization=campagne,
        period=period,
    )
    folder_model1 = FolderModel.objects.create(
        name="Modèle de dossier valorisé", project=project1
    )
    status1 = Status.objects.create(
        name="Structure à contacter 1", folder_model=folder_model1, order=0
    )
    status2 = Status.objects.create(
        name="Structure contactée 1", folder_model=folder_model1, order=1
    )
    status3 = Status.objects.create(
        name="Structure formée 1", folder_model=folder_model1, order=2
    )
    status4 = Status.objects.create(
        name="Structure partenaire 1", folder_model=folder_model1, order=3
    )
    category_model_1 = CategoryModel.objects.create(
        name="Démarchage", folder_model=folder_model1, order=0
    )
    category_model_2 = CategoryModel.objects.create(
        name="Rendez-vous approfondi", folder_model=folder_model1, order=1
    )
    category_model_3 = CategoryModel.objects.create(
        name="Formation", folder_model=folder_model1, order=2
    )
    category_model_4 = CategoryModel.objects.create(
        name="Formalisation du partenariat", folder_model=folder_model1, order=3
    )
    action_model1 = ActionModel.objects.create(
        name="Porte à porte",
        category_model=category_model_1,
        default=True,
        order=0,
        coefficient_enabled=True,
    )
    action_model1.valorizations.add(valorization_act1_ville)
    action_model1.valorizations.add(valorization_act1_campagne)
    action_model2 = ActionModel.objects.create(
        name="Rendez-vous",
        trigger_status=status2,
        category_model=category_model_2,
        default=True,
        optional=True,
        order=0,
    )
    action_model2.valorizations.add(valorization_act1_ville)
    action_model2.valorizations.add(valorization_act1_campagne)
    action_model3 = ActionModel.objects.create(
        name="Réunion d'information",
        trigger_status=status3,
        category_model=category_model_3,
        default=True,
        order=0,
    )
    action_model3.valorizations.add(valorization_act2_ville)
    action_model3.valorizations.add(valorization_act2_campagne)
    action_model5 = ActionModel.objects.create(
        name="Formation",
        trigger_status=status3,
        category_model=category_model_3,
        default=True,
        order=1,
    )
    action_model5.valorizations.add(valorization_horaire1_ville)
    action_model5.valorizations.add(valorization_horaire1_campagne)
    action_model6 = ActionModel.objects.create(
        name="Préparation de la charte",
        category_model=category_model_4,
        default=True,
        order=0,
    )
    action_model6.valorizations.add(valorization_horaire1_ville)
    action_model6.valorizations.add(valorization_horaire1_campagne)
    action_model7 = ActionModel.objects.create(
        name="Signature d'une charte",
        trigger_status=status4,
        category_model=category_model_4,
        default=True,
        order=1,
    )
    action_model7.valorizations.add(valorization_horaire1_ville)
    action_model7.valorizations.add(valorization_horaire1_campagne)
    action_model8 = ActionModel.objects.create(
        name="Préco'immo",
        trigger_status=status4,
        category_model=category_model_4,
        default=True,
        order=2,
    )
    action_model8.valorizations.add(valorization_horaire2_ville)
    action_model8.valorizations.add(valorization_horaire2_campagne)
    action_model9 = ActionModel.objects.create(
        name="Participation à un événement",
        category_model=category_model_4,
        optional=True,
        order=0,
        coefficient_enabled=True,
    )
    action_model9.valorizations.add(valorization_horaire2_ville)
    action_model9.valorizations.add(valorization_horaire2_campagne)
    action_model10 = ActionModel.objects.create(
        name="Rédaction communication article",
        category_model=category_model_4,
        optional=True,
        order=1,
    )
    action_model10.valorizations.add(valorization_horaire2_ville)
    action_model10.valorizations.add(valorization_horaire2_campagne)
    contact_content_type = ContentType.objects.get(app_label="fac", model="contact")
    orga_content_type = ContentType.objects.get(app_label="fac", model="organization")
    folder1 = Folder.objects.create(
        description="Dossier avec valorisation 1",
        model=folder_model1,
        owning_group=laureate_group1,
        type_valorization=ville,
        object_id=orga.pk,
        content_type=orga_content_type,
    )
    folder2 = Folder.objects.create(
        description="Dossier avec valorisation 1",
        model=folder_model1,
        owning_group=laureate_group2,
        type_valorization=ville,
        object_id=marie.pk,
        content_type=contact_content_type,
    )
    ObjectiveStatus.objects.create(
        name="obj status1",
        period=period,
        group=laureate_group1,
        status=status1,
        nb_statuses=150,
    )
    ObjectiveStatus.objects.create(
        name="obj status2",
        period=period,
        group=laureate_group1,
        status=status2,
        nb_statuses=150,
    )
    ObjectiveStatus.objects.create(
        name="obj status3",
        period=period,
        group=laureate_group1,
        status=status3,
        nb_statuses=100,
    )
    ObjectiveStatus.objects.create(
        name="obj status4",
        period=period,
        group=laureate_group1,
        status=status4,
        nb_statuses=75,
    )
    ObjectiveStatus.objects.create(
        name="obj status1",
        period=period,
        group=laureate_group2,
        status=status1,
        nb_statuses=150,
    )
    ObjectiveStatus.objects.create(
        name="obj status2",
        period=period,
        group=laureate_group2,
        status=status2,
        nb_statuses=150,
    )
    ObjectiveStatus.objects.create(
        name="obj status3",
        period=period,
        group=laureate_group2,
        status=status3,
        nb_statuses=100,
    )
    ObjectiveStatus.objects.create(
        name="obj status4",
        period=period,
        group=laureate_group2,
        status=status4,
        nb_statuses=75,
    )
    # Objective action
    ObjectiveAction.objects.create(
        name="obj action1",
        period=period,
        group=laureate_group2,
        model_action=action_model1,
        nb_actions=150,
    )
    ObjectiveAction.objects.create(
        name="obj action2",
        period=period,
        group=laureate_group2,
        model_action=action_model2,
        nb_actions=150,
    )
    ObjectiveAction.objects.create(
        name="obj action3",
        period=period,
        group=laureate_group2,
        model_action=action_model3,
        nb_actions=100,
    )
    ObjectiveAction.objects.create(
        name="obj action5",
        period=period,
        group=laureate_group2,
        model_action=action_model5,
        nb_actions=150,
    )
    ObjectiveAction.objects.create(
        name="obj action6",
        period=period,
        group=laureate_group2,
        model_action=action_model6,
        nb_actions=150,
    )
    ObjectiveAction.objects.create(
        name="obj action7",
        period=period,
        group=laureate_group2,
        model_action=action_model7,
        nb_actions=100,
    )
    ObjectiveAction.objects.create(
        name="obj action8",
        period=period,
        group=laureate_group2,
        model_action=action_model8,
        nb_actions=75,
    )
    ObjectiveAction.objects.create(
        name="obj action9",
        period=period,
        group=laureate_group2,
        model_action=action_model9,
        nb_actions=75,
    )
    for i in range(0, 100):
        Action.objects.create(
            duration=int(random.random() * 50) / 5,
            date=date(year=2020, month=1, day=1) + timedelta(days=i),
            done=True,
            done_by=jean_conseiller,
            message=f"action {i}",
            folder=folder1,
            model=action_model1,
            valorization=valorization_act1_ville,
        )
        Action.objects.create(
            duration=int(random.random() * 50) / 5,
            date=date(year=2020, month=1, day=1) + timedelta(days=i),
            done=True,
            done_by=jean_conseiller,
            message=f"action {i}",
            folder=folder2,
            model=action_model1,
            valorization=valorization_act1_campagne,
        )
    for i in range(100, 180):
        Action.objects.create(
            duration=int(random.random() * 50) / 5,
            date=date(year=2020, month=1, day=1) + timedelta(days=i),
            done=True,
            done_by=jean_conseiller,
            message=f"action {i}",
            folder=folder1,
            model=action_model2,
            valorization=valorization_act1_ville,
        )
        Action.objects.create(
            duration=int(random.random() * 50) / 5,
            date=date(year=2020, month=1, day=1) + timedelta(days=i),
            done=True,
            done_by=jean_conseiller,
            message=f"action {i}",
            folder=folder2,
            model=action_model2,
            valorization=valorization_act1_campagne,
        )
    for i in range(180, 240):
        Action.objects.create(
            duration=int(random.random() * 50) / 5,
            date=date(year=2020, month=1, day=1) + timedelta(days=i),
            done=True,
            done_by=jean_conseiller,
            message=f"action {i}",
            folder=folder1,
            model=action_model3,
            valorization=valorization_act2_ville,
        )
        Action.objects.create(
            duration=int(random.random() * 50) / 5,
            date=date(year=2020, month=1, day=1) + timedelta(days=i),
            done=True,
            done_by=jean_conseiller,
            message=f"action {i}",
            folder=folder2,
            model=action_model3,
            valorization=valorization_act2_campagne,
        )
    for i in range(240, 280):
        Action.objects.create(
            duration=int(random.random() * 50) / 5,
            date=date(year=2020, month=1, day=1) + timedelta(days=i),
            done=True,
            done_by=jean_conseiller,
            message=f"action {i}",
            folder=folder1,
            model=action_model2,
            valorization=valorization_act1_ville,
        )
        Action.objects.create(
            duration=int(random.random() * 50) / 5,
            date=date(year=2020, month=1, day=1) + timedelta(days=i),
            done=True,
            done_by=jean_conseiller,
            message=f"action {i}",
            folder=folder2,
            model=action_model2,
            valorization=valorization_act1_campagne,
        )
    for i in range(280, 300):
        Action.objects.create(
            duration=int(random.random() * 50) / 5,
            date=date(year=2020, month=1, day=1) + timedelta(days=i),
            done=True,
            done_by=jean_conseiller,
            message=f"action {i}",
            folder=folder1,
            model=action_model5,
            valorization=valorization_horaire1_ville,
        )
        Action.objects.create(
            duration=int(random.random() * 50) / 5,
            date=date(year=2020, month=1, day=1) + timedelta(days=i),
            done=True,
            done_by=jean_conseiller,
            message=f"action {i}",
            folder=folder2,
            model=action_model5,
            valorization=valorization_horaire1_campagne,
        )
    for i in range(300, 310):
        Action.objects.create(
            duration=int(random.random() * 50) / 5,
            date=date(year=2020, month=1, day=1) + timedelta(days=i),
            done=True,
            done_by=jean_conseiller,
            message=f"action {i}",
            folder=folder1,
            model=action_model6,
            valorization=valorization_horaire1_ville,
        )
    for i in range(310, 320):
        Action.objects.create(
            duration=int(random.random() * 50) / 5,
            date=date(year=2020, month=1, day=1) + timedelta(days=i),
            done=True,
            done_by=jean_conseiller,
            message=f"action {i}",
            folder=folder1,
            model=action_model6,
            valorization=valorization_horaire1_ville,
        )
        Action.objects.create(
            duration=int(random.random() * 50) / 5,
            date=date(year=2020, month=1, day=1) + timedelta(days=i),
            done=True,
            done_by=jean_conseiller,
            message=f"action {i}",
            folder=folder2,
            model=action_model6,
            valorization=valorization_horaire1_campagne,
        )
    for i in range(320, 330):
        Action.objects.create(
            duration=int(random.random() * 50) / 5,
            date=date(year=2020, month=1, day=1) + timedelta(days=i),
            done=True,
            done_by=jean_conseiller,
            message=f"action {i}",
            folder=folder1,
            model=action_model6,
            valorization=valorization_horaire1_ville,
        )
    for i in range(330, 340):
        Action.objects.create(
            duration=int(random.random() * 50) / 5,
            date=date(year=2020, month=1, day=1) + timedelta(days=i),
            done=True,
            done_by=jean_conseiller,
            message=f"action {i}",
            folder=folder1,
            model=action_model7,
            valorization=valorization_horaire1_ville,
        )
        Action.objects.create(
            duration=int(random.random() * 50) / 5,
            date=date(year=2020, month=1, day=1) + timedelta(days=i),
            done=True,
            done_by=jean_conseiller,
            message=f"action {i}",
            folder=folder2,
            model=action_model7,
            valorization=valorization_horaire1_campagne,
        )
    for i in range(340, 350):
        Action.objects.create(
            duration=int(random.random() * 50) / 5,
            date=date(year=2020, month=1, day=1) + timedelta(days=i),
            done=True,
            done_by=jean_conseiller,
            message=f"action {i}",
            folder=folder1,
            model=action_model8,
            valorization=valorization_act2_ville,
        )
        Action.objects.create(
            duration=int(random.random() * 50) / 5,
            date=date(year=2020, month=1, day=1) + timedelta(days=i),
            done=True,
            done_by=jean_conseiller,
            message=f"action {i}",
            folder=folder2,
            model=action_model8,
            valorization=valorization_horaire2_campagne,
        )
    for i in range(350, 360):
        Action.objects.create(
            duration=int(random.random() * 50) / 5,
            date=date(year=2020, month=1, day=1) + timedelta(days=i),
            done=True,
            done_by=jean_conseiller,
            message=f"action {i}",
            folder=folder1,
            model=action_model9,
            valorization=valorization_horaire2_ville,
        )
        Action.objects.create(
            duration=int(random.random() * 50) / 5,
            date=date(year=2020, month=1, day=1) + timedelta(days=i),
            done=True,
            done_by=jean_conseiller,
            message=f"action {i}",
            folder=folder2,
            model=action_model9,
            valorization=valorization_horaire2_campagne,
        )
    for i in range(360, 370):
        Action.objects.create(
            duration=int(random.random() * 50) / 5,
            date=date(year=2020, month=1, day=1) + timedelta(days=i),
            done=True,
            done_by=jean_conseiller,
            message=f"action {i}",
            folder=folder1,
            model=action_model10,
            valorization=valorization_horaire2_ville,
        )
        Action.objects.create(
            duration=int(random.random() * 50) / 5,
            date=date(year=2020, month=1, day=1) + timedelta(days=i),
            done=True,
            done_by=jean_conseiller,
            message=f"action {i}",
            folder=folder2,
            model=action_model10,
            valorization=valorization_horaire2_campagne,
        )


def generate_entries_objectives():  # noqa: C901
    # project without valorization and budget
    project1 = Project.objects.create(name="projet sans valorisations")
    project1.groups.add(pilot_group)
    folder_model1 = FolderModel.objects.create(
        name="Modèle de dossier avec objectif", project=project1
    )
    status1 = Status.objects.create(
        name="Structure à contacter 2", folder_model=folder_model1, order=0
    )
    status2 = Status.objects.create(
        name="Structure contactée 2", folder_model=folder_model1, order=1
    )
    status3 = Status.objects.create(
        name="Structure formée 2", folder_model=folder_model1, order=2
    )
    status4 = Status.objects.create(
        name="Structure partenaire 2", folder_model=folder_model1, order=3
    )
    category_model_1 = CategoryModel.objects.create(
        name="Démarchage 2", folder_model=folder_model1, order=0
    )
    category_model_2 = CategoryModel.objects.create(
        name="Rendez-vous approfondi 2", folder_model=folder_model1, order=1
    )
    category_model_3 = CategoryModel.objects.create(
        name="Formation 2", folder_model=folder_model1, order=2
    )
    category_model_4 = CategoryModel.objects.create(
        name="Formalisation du partenariat 2", folder_model=folder_model1, order=3
    )
    action_model1 = ActionModel.objects.create(
        name="Porte à porte 2", category_model=category_model_1, default=True, order=0
    )
    action_model2 = ActionModel.objects.create(
        name="Rendez-vous 2",
        trigger_status=status2,
        category_model=category_model_2,
        default=True,
        optional=True,
        order=0,
    )
    action_model3 = ActionModel.objects.create(
        name="Réunion d'information 2",
        trigger_status=status3,
        category_model=category_model_3,
        default=True,
        order=0,
    )
    action_model5 = ActionModel.objects.create(
        name="Formation 2",
        trigger_status=status3,
        category_model=category_model_3,
        default=True,
        order=1,
    )
    action_model6 = ActionModel.objects.create(
        name="Préparation de la charte 2",
        category_model=category_model_4,
        default=True,
        order=0,
    )
    action_model7 = ActionModel.objects.create(
        name="Signature d'une charte 2",
        trigger_status=status4,
        category_model=category_model_4,
        default=True,
        order=1,
    )
    action_model8 = ActionModel.objects.create(
        name="Préco'immo 2",
        trigger_status=status4,
        category_model=category_model_4,
        default=True,
        order=2,
    )
    action_model9 = ActionModel.objects.create(
        name="Participation à un événement 2",
        category_model=category_model_4,
        optional=True,
        order=0,
    )
    action_model10 = ActionModel.objects.create(
        name="Rédaction communication article 2",
        category_model=category_model_4,
        optional=True,
        order=1,
    )
    contact_content_type = ContentType.objects.get(app_label="fac", model="contact")
    folder1 = Folder.objects.create(
        description="Dossier avec valorisation 2",
        model=folder_model1,
        owning_group=pilot_group,
        object_id=marie.pk,
        content_type=contact_content_type,
    )
    ObjectiveStatus.objects.create(
        name="obj status5",
        period=period,
        group=pilot_group,
        status=status1,
        nb_statuses=150,
    )
    ObjectiveStatus.objects.create(
        name="obj status6",
        period=period,
        group=pilot_group,
        status=status2,
        nb_statuses=150,
    )
    ObjectiveStatus.objects.create(
        name="obj status7",
        period=period,
        group=pilot_group,
        status=status3,
        nb_statuses=100,
    )
    ObjectiveStatus.objects.create(
        name="obj status8",
        period=period,
        group=pilot_group,
        status=status4,
        nb_statuses=75,
    )
    ObjectiveAction.objects.create(
        name="obj action1",
        period=period,
        group=pilot_group,
        model_action=action_model1,
        nb_actions=150,
    )
    ObjectiveAction.objects.create(
        name="obj action2",
        period=period,
        group=pilot_group,
        model_action=action_model2,
        nb_actions=150,
    )
    ObjectiveAction.objects.create(
        name="obj action3",
        period=period,
        group=pilot_group,
        model_action=action_model3,
        nb_actions=100,
    )
    ObjectiveAction.objects.create(
        name="obj action5",
        period=period,
        group=pilot_group,
        model_action=action_model5,
        nb_actions=150,
    )
    ObjectiveAction.objects.create(
        name="obj action6",
        period=period,
        group=pilot_group,
        model_action=action_model6,
        nb_actions=150,
    )
    ObjectiveAction.objects.create(
        name="obj action7",
        period=period,
        group=pilot_group,
        model_action=action_model7,
        nb_actions=100,
    )
    ObjectiveAction.objects.create(
        name="obj action8",
        period=period,
        group=pilot_group,
        model_action=action_model8,
        nb_actions=75,
    )
    ObjectiveAction.objects.create(
        name="obj action9",
        period=period,
        group=pilot_group,
        model_action=action_model9,
        nb_actions=75,
    )
    for i in range(0, 100):
        Action.objects.create(
            duration=int(random.random() * 50) / 5,
            date=date(year=2020, month=1, day=1) + timedelta(days=i),
            done=True,
            done_by=jean_conseiller,
            message=f"action 2-{i}",
            folder=folder1,
            model=action_model1,
        )
    for i in range(100, 180):
        Action.objects.create(
            duration=int(random.random() * 50) / 5,
            date=date(year=2020, month=1, day=1) + timedelta(days=i),
            done=True,
            done_by=jean_conseiller,
            message=f"action 2-{i}",
            folder=folder1,
            model=action_model2,
        )
    for i in range(180, 240):
        Action.objects.create(
            duration=int(random.random() * 50) / 5,
            date=date(year=2020, month=1, day=1) + timedelta(days=i),
            done=True,
            done_by=jean_conseiller,
            message=f"action 2-{i}",
            folder=folder1,
            model=action_model3,
        )
    for i in range(240, 280):
        Action.objects.create(
            duration=int(random.random() * 50) / 5,
            date=date(year=2020, month=1, day=1) + timedelta(days=i),
            done=True,
            done_by=jean_conseiller,
            message=f"action 2-{i}",
            folder=folder1,
            model=action_model2,
        )
    for i in range(280, 300):
        Action.objects.create(
            duration=int(random.random() * 50) / 5,
            date=date(year=2020, month=1, day=1) + timedelta(days=i),
            done=True,
            done_by=jean_conseiller,
            message=f"action 2-{i}",
            folder=folder1,
            model=action_model5,
        )
    for i in range(300, 310):
        Action.objects.create(
            duration=int(random.random() * 50) / 5,
            date=date(year=2020, month=1, day=1) + timedelta(days=i),
            done=True,
            done_by=jean_conseiller,
            message=f"action 2-{i}",
            folder=folder1,
            model=action_model6,
        )
    for i in range(310, 320):
        Action.objects.create(
            duration=int(random.random() * 50) / 5,
            date=date(year=2020, month=1, day=1) + timedelta(days=i),
            done=True,
            done_by=jean_conseiller,
            message=f"action 2-{i}",
            folder=folder1,
            model=action_model6,
        )
    for i in range(320, 330):
        Action.objects.create(
            duration=int(random.random() * 50) / 5,
            date=date(year=2020, month=1, day=1) + timedelta(days=i),
            done=True,
            done_by=jean_conseiller,
            message=f"action 2-{i}",
            folder=folder1,
            model=action_model6,
        )
    for i in range(330, 340):
        Action.objects.create(
            duration=int(random.random() * 50) / 5,
            date=date(year=2020, month=1, day=1) + timedelta(days=i),
            done=True,
            done_by=jean_conseiller,
            message=f"action 2-{i}",
            folder=folder1,
            model=action_model7,
        )
    for i in range(340, 350):
        Action.objects.create(
            duration=int(random.random() * 50) / 5,
            date=date(year=2020, month=1, day=1) + timedelta(days=i),
            done=True,
            done_by=jean_conseiller,
            message=f"action 2-{i}",
            folder=folder1,
            model=action_model8,
        )
    for i in range(350, 360):
        Action.objects.create(
            duration=int(random.random() * 50) / 5,
            date=date(year=2020, month=1, day=1) + timedelta(days=i),
            done=True,
            done_by=jean_conseiller,
            message=f"action 2-{i}",
            folder=folder1,
            model=action_model9,
        )
    for i in range(360, 370):
        Action.objects.create(
            duration=int(random.random() * 50) / 5,
            date=date(year=2020, month=1, day=1) + timedelta(days=i),
            done=True,
            done_by=jean_conseiller,
            message=f"action 2-{i}",
            folder=folder1,
            model=action_model10,
        )


def generate_entries_no_period():  # noqa: C901
    project1 = Project.objects.create(name="projet sans période")
    project1.groups.add(pilot_group)
    folder_model1 = FolderModel.objects.create(
        name="Modèle de dossier sans objectif 3", project=project1
    )
    Status.objects.create(
        name="Structure à contacter 3", folder_model=folder_model1, order=0
    )
    status2 = Status.objects.create(
        name="Structure contactée 3", folder_model=folder_model1, order=1
    )
    status3 = Status.objects.create(
        name="Structure formée 3", folder_model=folder_model1, order=2
    )
    status4 = Status.objects.create(
        name="Structure partenaire 3", folder_model=folder_model1, order=3
    )
    category_model_1 = CategoryModel.objects.create(
        name="Démarchage 3", folder_model=folder_model1, order=0
    )
    category_model_2 = CategoryModel.objects.create(
        name="Rendez-vous approfondi 3", folder_model=folder_model1, order=1
    )
    category_model_3 = CategoryModel.objects.create(
        name="Formation 3", folder_model=folder_model1, order=2
    )
    category_model_4 = CategoryModel.objects.create(
        name="Formalisation du partenariat 3", folder_model=folder_model1, order=3
    )
    action_model1 = ActionModel.objects.create(
        name="Porte à porte 3", category_model=category_model_1, default=True, order=0
    )
    action_model2 = ActionModel.objects.create(
        name="Rendez-vous 3",
        trigger_status=status2,
        category_model=category_model_2,
        default=True,
        optional=True,
        order=0,
    )
    action_model3 = ActionModel.objects.create(
        name="Réunion d'information 3",
        trigger_status=status3,
        category_model=category_model_3,
        default=True,
        order=0,
    )
    action_model5 = ActionModel.objects.create(
        name="Formation 3",
        trigger_status=status3,
        category_model=category_model_3,
        default=True,
        order=1,
    )
    action_model6 = ActionModel.objects.create(
        name="Préparation de la charte 3",
        category_model=category_model_4,
        default=True,
        order=0,
    )
    action_model7 = ActionModel.objects.create(
        name="Signature d'une charte 3",
        trigger_status=status4,
        category_model=category_model_4,
        default=True,
        order=1,
    )
    action_model8 = ActionModel.objects.create(
        name="Préco'immo 3",
        trigger_status=status4,
        category_model=category_model_4,
        default=True,
        order=2,
    )
    action_model9 = ActionModel.objects.create(
        name="Participation à un événement 3",
        category_model=category_model_4,
        optional=True,
        order=0,
    )
    action_model10 = ActionModel.objects.create(
        name="Rédaction communication article 3",
        category_model=category_model_4,
        optional=True,
        order=1,
    )
    contact_content_type = ContentType.objects.get(app_label="fac", model="contact")
    orga_content_type = ContentType.objects.get(app_label="fac", model="organization")
    folder1 = Folder.objects.create(
        description="Dossier avec valorisation 3",
        model=folder_model1,
        owning_group=pilot_group,
        object_id=marie.pk,
        content_type=contact_content_type,
    )
    folder2 = Folder.objects.create(
        description="Dossier avec valorisation 4",
        model=folder_model1,
        owning_group=pilot_group,
        object_id=orga.pk,
        content_type=orga_content_type,
    )
    for i in range(0, 100):
        Action.objects.create(
            duration=int(random.random() * 50) / 5,
            date=date(year=2020, month=1, day=1) + timedelta(days=i),
            done=True,
            done_by=jean_conseiller,
            message=f"action 3-{i}",
            folder=folder1,
            model=action_model1,
        )
    for i in range(100, 180):
        Action.objects.create(
            duration=int(random.random() * 50) / 5,
            date=date(year=2020, month=1, day=1) + timedelta(days=i),
            done=True,
            done_by=jean_conseiller,
            message=f"action 3-{i}",
            folder=folder1,
            model=action_model2,
        )
    for i in range(180, 240):
        Action.objects.create(
            duration=int(random.random() * 50) / 5,
            date=date(year=2020, month=1, day=1) + timedelta(days=i),
            done=True,
            done_by=jean_conseiller,
            message=f"action 3-{i}",
            folder=folder1,
            model=action_model3,
        )
    for i in range(240, 280):
        Action.objects.create(
            duration=int(random.random() * 50) / 5,
            date=date(year=2020, month=1, day=1) + timedelta(days=i),
            done=True,
            done_by=jean_conseiller,
            message=f"action 3-{i}",
            folder=folder2,
            model=action_model2,
        )
    for i in range(280, 300):
        Action.objects.create(
            duration=int(random.random() * 50) / 5,
            date=date(year=2020, month=1, day=1) + timedelta(days=i),
            done=True,
            done_by=jean_conseiller,
            message=f"action 3-{i}",
            folder=folder2,
            model=action_model5,
        )
    for i in range(300, 310):
        Action.objects.create(
            duration=int(random.random() * 50) / 5,
            date=date(year=2020, month=1, day=1) + timedelta(days=i),
            done=True,
            done_by=jean_conseiller,
            message=f"action 3-{i}",
            folder=folder2,
            model=action_model6,
        )
    for i in range(310, 320):
        Action.objects.create(
            duration=int(random.random() * 50) / 5,
            date=date(year=2020, month=1, day=1) + timedelta(days=i),
            done=True,
            done_by=jean_conseiller,
            message=f"action 3-{i}",
            folder=folder2,
            model=action_model6,
        )
    for i in range(320, 330):
        Action.objects.create(
            duration=int(random.random() * 50) / 5,
            date=date(year=2020, month=1, day=1) + timedelta(days=i),
            done=True,
            done_by=jean_conseiller,
            message=f"action 3-{i}",
            folder=folder2,
            model=action_model6,
        )
    for i in range(330, 340):
        Action.objects.create(
            duration=int(random.random() * 50) / 5,
            date=date(year=2020, month=1, day=1) + timedelta(days=i),
            done=True,
            done_by=jean_conseiller,
            message=f"action 3-{i}",
            folder=folder2,
            model=action_model7,
        )
    for i in range(340, 350):
        Action.objects.create(
            duration=int(random.random() * 50) / 5,
            date=date(year=2020, month=1, day=1) + timedelta(days=i),
            done=True,
            done_by=jean_conseiller,
            message=f"action 3-{i}",
            folder=folder2,
            model=action_model8,
        )
    for i in range(350, 360):
        Action.objects.create(
            duration=int(random.random() * 50) / 5,
            date=date(year=2020, month=1, day=1) + timedelta(days=i),
            done=True,
            done_by=jean_conseiller,
            message=f"action 3-{i}",
            folder=folder2,
            model=action_model9,
        )
    for i in range(360, 370):
        Action.objects.create(
            duration=int(random.random() * 50) / 5,
            date=date(year=2020, month=1, day=1) + timedelta(days=i),
            done=True,
            done_by=jean_conseiller,
            message=f"action 3-{i}",
            folder=folder2,
            model=action_model10,
        )


if __name__ == "__main__":
    entry = input(
        "Careful! This will generate tons of sample entries in your database. "
        "Type 'YAS-I-AM-SURE' to continue."
    )
    if entry.strip() == "YAS-I-AM-SURE":
        create_commons()
        generate_entries_valorizations()
        generate_entries_objectives()
        generate_entries_no_period()

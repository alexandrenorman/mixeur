from django.contrib.postgres.fields.jsonb import KeyTextTransform

from fac.models import Action

from helpers.strings import print_boxed


def get_custom_data(custom_form_data, key):
    return (
        custom_form_data[key]
        if custom_form_data is not None and key in custom_form_data
        else ""
    )


class ExportSare:
    def __init__(self, group_pk: int = None):
        self.group_pk = group_pk

    def adapters(self):
        return {
            "act_type": ExportSare._convert_act_type,
        }

    @staticmethod
    def _convert_act_type(value, *args, **kwargs):
        try:
            act = value.split("-")[0].strip()
        except Exception:
            return value

        translate = {
            "A1": "A01",
            "A2": "A02",
            "A3": "A03",
            "A4": "A04",
            "A4 bis": "A4b",
            "A5": "A05",
            "B1": "B01",
            "B2": "B02",
        }
        if act in translate:
            return translate[act]

        return act

    def objects(self):
        objects = []
        for obj in self.queryset():
            values = {
                "ID": f"mixeur.fac.action.{obj.pk}",
                "folder__owning_group__ademe_id": obj.folder.owning_group.ademe_id
                or obj.folder.owning_group.name,
                "date": obj.date,
                "duration": int(obj.duration * 60),
                "duration_unit": "M",
                "done_by__full_name": "",
                "folder__owning_group__name": obj.folder.owning_group.name,
                "model__name": obj.model.name,
                "updated_at": obj.updated_at,
                "linked_object__address": "",
                "linked_object__email": "",
                "linked_object__first_name": "",
                "linked_object__last_name": "",
                "linked_object__phone": "",
                "linked_object__siret": "",
                "linked_object__name": "",
                "linked_object__town": "",
                "linked_object__zipcode": "",
                "linked_object__inseecode": "",
                "custom_form_data__d_034": obj.custom_form_data__d_034,
                "custom_form_data__d_035": obj.custom_form_data__d_035,
                # Same field 36 for A1 and 80 for B1
                "custom_form_data__d_036": obj.custom_form_data__d_036
                or obj.custom_form_data__d_080,
                # Same field 37 for A1 and 81 for B1
                "custom_form_data__d_037": obj.custom_form_data__d_037
                or obj.custom_form_data__d_081,
                # Same field 43 for A2 and 87 for B2
                "custom_form_data__d_043": obj.custom_form_data__d_043
                or obj.custom_form_data__d_087,
                "custom_form_data__d_044b": obj.custom_form_data__d_044b,
                "custom_form_data__d_046": obj.custom_form_data__d_046,
                "custom_form_data__d_049": obj.custom_form_data__d_049,
                "custom_form_data__d_050": obj.custom_form_data__d_050,
                "custom_form_data__d_052": obj.custom_form_data__d_052,
                "custom_form_data__d_058": obj.custom_form_data__d_058,
                "custom_form_data__d_060": obj.custom_form_data__d_060,
                "custom_form_data__d_063": obj.custom_form_data__d_063,
                "custom_form_data__d_065": obj.custom_form_data__d_065,
                "custom_form_data__d_067": obj.custom_form_data__d_067,
                "custom_form_data__d_085": obj.custom_form_data__d_085,
                "custom_form_data__siret": obj.custom_form_data__siret,
                "custom_form_data__d_012": "",  # contact
                "custom_form_data__d_015": "",  # contact
                "custom_form_data__d_029": "",  # contact
                "custom_form_data__d_074": "",  # contact
                "custom_form_data__public_type": "",
                "technical_update_date": None,
            }

            if obj.done_by is not None:
                values["done_by__full_name"] = obj.done_by.full_name

            if obj.linked_object is not None:
                values["linked_object__address"] = obj.linked_object.address
                values["linked_object__email"] = obj.linked_object.email
                values["linked_object__phone"] = obj.linked_object.phone
                values["linked_object__town"] = obj.linked_object.town
                values["linked_object__zipcode"] = obj.linked_object.zipcode
                values["linked_object__inseecode"] = obj.linked_object.inseecode

                if obj.linked_object.__class__.__name__ == "Contact":
                    values["linked_object__first_name"] = obj.linked_object.first_name
                    values["linked_object__last_name"] = obj.linked_object.last_name

                elif obj.linked_object.__class__.__name__ == "Organization":
                    values["linked_object__name"] = obj.linked_object.name

                if obj.linked_object.__class__.__name__ in ["Contact", "Organization"]:
                    values["custom_form_data__public_type"] = get_custom_data(
                        obj.linked_object.custom_form_data, "public_type"
                    )
                    values["custom_form_data__d_012"] = get_custom_data(
                        obj.linked_object.custom_form_data, "d_012"
                    )
                    values["custom_form_data__d_015"] = get_custom_data(
                        obj.linked_object.custom_form_data, "d_015"
                    )
                    values["custom_form_data__d_029"] = get_custom_data(
                        obj.linked_object.custom_form_data, "d_029"
                    )
                    values["custom_form_data__d_074"] = get_custom_data(
                        obj.linked_object.custom_form_data, "d_074"
                    )

                else:
                    print_boxed(
                        f"Error : unknown class {obj.linked_object.__class__.__name__}"
                    )

            objects.append(values)

        return objects

    def queryset(self):
        qs = Action.objects.all()

        if self.group_pk is not None:
            qs = qs.filter(
                folder__owning_group=self.group_pk,
            )

        qs = (
            qs.filter(
                folder__model__project__name="Programme SARE",
                done=True,
            )
            .exclude(model__name__in=["Commentaire", "Projet terminé"])
            .order_by("updated_at")
            .annotate(
                custom_form_data__d_034=KeyTextTransform("d_034", "custom_form_data"),
                custom_form_data__d_035=KeyTextTransform("d_035", "custom_form_data"),
                custom_form_data__d_036=KeyTextTransform(
                    "d_036", "custom_form_data"
                ),  # see d_080
                custom_form_data__d_037=KeyTextTransform(
                    "d_037", "custom_form_data"
                ),  # see d_081
                custom_form_data__d_043=KeyTextTransform(
                    "d_043", "custom_form_data"
                ),  # see d_087 !
                custom_form_data__d_044b=KeyTextTransform("d_044b", "custom_form_data"),
                custom_form_data__d_046=KeyTextTransform("d_046", "custom_form_data"),
                custom_form_data__d_049=KeyTextTransform("d_049", "custom_form_data"),
                custom_form_data__d_050=KeyTextTransform("d_050", "custom_form_data"),
                custom_form_data__d_052=KeyTextTransform("d_052", "custom_form_data"),
                custom_form_data__d_058=KeyTextTransform("d_058", "custom_form_data"),
                custom_form_data__d_060=KeyTextTransform("d_060", "custom_form_data"),
                custom_form_data__d_063=KeyTextTransform("d_063", "custom_form_data"),
                custom_form_data__d_065=KeyTextTransform("d_065", "custom_form_data"),
                custom_form_data__d_067=KeyTextTransform("d_067", "custom_form_data"),
                custom_form_data__d_080=KeyTextTransform("d_080", "custom_form_data"),
                custom_form_data__d_081=KeyTextTransform("d_081", "custom_form_data"),
                custom_form_data__d_085=KeyTextTransform("d_085", "custom_form_data"),
                custom_form_data__d_087=KeyTextTransform(
                    "d_087", "custom_form_data"
                ),  # see d_043 !
                custom_form_data__siret=KeyTextTransform("d_069", "custom_form_data"),
            )
        )
        return qs

    @staticmethod  # NOQA: CFQ001
    def columns():
        columns = [
            {"field": "ID", "title": "1 - Identifiant unique de l'acte"},
            {
                "field": "folder__owning_group__ademe_id",
                "title": "2 - Structure",
                "fct": "truncate",
                "arg": 100,
            },
            {
                "field": "done_by__full_name",
                "title": "3 - Conseiller",
                "fct": "truncate",
                "arg": 100,
            },
            {
                "field": "model__name",
                "title": "4 - Type Acte",
                "fct": "act_type",
            },
            {
                "field": "date",
                "title": "5 - Date Acte",
                "fct": "date",
                "arg": "%Y-%m-%d",
            },
            {"field": "duration", "title": "6 - Durée Acte"},
            {
                "field": "duration_unit",
                "title": "7 - Unité Durée Acte",
                "fct": "nop",
            },
            {
                "field": "custom_form_data__public_type",
                "title": "8 - Type de public",
                "fct": "list",
                "arg": {
                    "PO": "PO",
                    "PB": "PB",
                    "Locataire": "LOCATAIRE",
                    "PO ou PB membre d’une SCI": "PO OU PB MEMBRE SCI",
                    "Occupant à titre gratuit": "OCCUPANT TITRE GRATUIT",
                    "Professionnel": "PROFESSIONNEL",
                    "Membre ou président de conseil syndical": "MEMBRE OU PRESIDENT DE CONSEIL SYNDICAL",
                    "SCI": "SCI",
                    "Syndic de copropriétés": "SYNDIC DE COPROPRIETE",
                    "Autre": "AUTRE",
                },
            },
            {
                "field": "linked_object__last_name",
                "title": "9 - Nom",
                "fct": "truncate",
                "arg": 100,
            },
            {
                "field": "linked_object__first_name",
                "title": "10 - Prénom",
                "fct": "truncate",
                "arg": 100,
            },
            {
                "field": "linked_object__name",
                "title": "11 - Raison sociale",
                "fct": "truncate",
                "arg": 100,
            },
            {
                "field": "custom_form_data__siret",
                "title": "12 - SIRET de l'entreprise ",
                "fct": "truncate",
                "arg": 14,
            },
            {
                "field": "custom_form_data__d_012",
                "title": "13 - Eligibilité aux aides Anah",
                "fct": "list",
                "arg": {"Oui": "OUI", "Non": "NON", "NSP": "NSP"},
            },
            {
                "field": "linked_object__email",
                "title": "14 - E-mail",
                "fct": "truncate",
                "arg": 100,
            },
            {
                "field": "linked_object__phone",
                "title": "15 - Téléphone",
                "fct": "truncate",
                "arg": 20,
            },
            {
                "field": "custom_form_data__d_015",
                "title": "16 - Type de logement",
                "fct": "list",
                "arg": {
                    "Logement individuel": "LI",
                    "Logement en copropriété": "LC",
                    "Copropriété": "CO",
                },
            },
            {
                "field": "custom_form_data__d_029",
                "title": "17 - Nombre de logement",
            },
            {
                "field": "linked_object__zipcode",
                "title": "18 - Code Postal",
                "fct": "truncate",
                "arg": 5,
            },
            {
                "field": "linked_object__town",
                "title": "19 - Commune",
                "fct": "truncate",
                "arg": 100,
            },
            {
                "field": "linked_object__address",
                "title": "20 - Adresse",
                "fct": "truncate",
                "arg": 100,
            },
            {
                "field": "custom_form_data__d_074",
                "title": "21 - Statut d'occupation",
                "fct": "list",
                "arg": {
                    "Locataire": "LOCATAIRE",
                    "Propriétaire": "PROPRIETAIRE",
                },
            },
            {
                "field": "custom_form_data__d_034",
                "title": "22 - Type de l'information",
                "fct": "list_multiple",
                "arg": {
                    "Information technique": "INFORMATION TECHNIQUE",
                    "Information financière": "INFORMATION FINANCIERE",
                    "Information juridique": "INFORMATION JURIDIQUE",
                    "Information sociale": "INFORMATION SOCIALE",
                },
            },
            {
                "field": "custom_form_data__d_035",
                "title": "23 - Nature de l'information",
                "fct": "list_multiple",
                "arg": {
                    "Informations générales": "INFORMATIONS GENERALES",
                    "Aides financières": "AIDES FINANCIERES",
                    "Demande à caractère économique et financier": "DEMANDE ECONOMIQUE ET FINANCIER",
                    "Thermographie": "THERMOGRAPHIE",
                    "Eco-gestes (économie d'eau, d'énergie...)": "ECOGESTES",
                    "Compréhension des factures d'énergie": "COMPREHENSION FACTURES ENERGIE",
                    "ENR": "ENR",
                    "Transport et mobilité": "TRANSPORT ET MOBILITE",
                    "Question techniques": "QUESTION TECHNIQUES",
                    "Réglementation/Législation": "REGLEMENTATION ET LEGISLATION",
                    "Construction": "CONSTRUCTION",
                    "Rénovation lourde": "RENOVATION LOURDE",
                    "Amélioration légère": "AMELIORATION LEGERE",
                    "Offres à 1€": "OFFRE 1 EURO",
                    "Démarchage": "DEMARCHAGE",
                    "Régulation": "REGULATION",
                    "Maintenance": "MAINTENANCE",
                    "Choix matériel": "CHOIX MATERIEL",
                    "Autre": "AUTRE",
                },
            },
            {
                "field": "custom_form_data__d_085",
                "title": "24 - Nature de l'information technique",
                "fct": "list_multiple",
                "arg": {
                    "Bâti": "BATI",
                    "Process": "PROCESS",
                    "Usages": "USAGES",
                },
            },
            # field « Question » is divided between
            # to custom forms fields d_036 (A1) and d_080 (B1)
            {
                "field": "custom_form_data__d_036",
                "title": "25 - Question (posée par le demandeur)",
                "fct": "html",
                "arg": 1000,
            },
            # field « Réponse » is divided between
            # to custom forms fields d_037 (A1) and d_081 (B1)
            {
                "field": "custom_form_data__d_037",
                "title": "26 - Réponse (apportée par le conseiller)",
                "fct": "html",
                "arg": 1000,
            },
            # field « Poursuite de service envisagée » is divided between
            # to custom forms fields d_043 (A2) and d_087 (B2)
            {
                "field": "custom_form_data__d_043",  # d_087
                "title": "27 - Poursuite de service envisagée",
                "fct": "list_multiple",
                "arg": {
                    "Réalisation d'un audit énergétique": "REALISATION AUDIT ENERGETIQUE",
                    "Accompagnement à la réalisation des travaux": "ACCOMPAGNEMENT REALISATION DE TRAVAUX",
                    "HMS": "HMS",
                    "Action Logement": "ACTION LOGEMENT",
                    "Accompagnement complet entreprise (MOE/AMO)": "ACCOMPAGNEMENT COMPLET ENTREPRISE (MOE/AMO)",
                    "Programme existant": "PROGRAMME EXISTANT",
                    "Action usage": "ACTION USAGES",
                    "Action bâti": "ACTION BATI",
                    "Action process": "ACTION PROCESS",
                    "Autre": "AUTRE",
                    "Pas de poursuite ": "PAS DE POURSUITE",
                    "Pas de poursuite ": "PAS DE POURSUITE",
                },
            },
            {
                "field": "custom_form_data__d_044b",
                "title": "28 - Rapport d'Audit / DTG remis au demandeur",
                "fct": "list",
                "arg": {"oui": "Oui", "non": "Non"},
            },
            {
                "field": "custom_form_data__d_046",
                "title": "29 - Visa conseiller",
                "fct": "list",
                "arg": {"oui": "Oui", "non": "Non"},
            },
            {
                "field": "custom_form_data__d_049",
                "title": "30 - Date de démarrage des travaux",
                "fct": "date",
                "arg": "%Y-%m-%d",
            },
            {
                "field": "custom_form_data__d_050",
                "title": "31 - Date du bilan de fin de travaux",
                "fct": "date",
                "arg": "%Y-%m-%d",
            },
            {
                "field": "custom_form_data__d_052",
                "title": "32 - Date abandon de l'accompagnement",
                "fct": "date",
                "arg": "%Y-%m-%d",
            },
            {
                "field": "custom_form_data__d_058",
                "title": "33 - Date de 1ere visite",
                "fct": "date",
                "arg": "%Y-%m-%d",
            },
            {
                "field": "custom_form_data__d_060",
                "title": "34 - Date du 1er devis",
                "fct": "date",
                "arg": "%Y-%m-%d",
            },
            {
                "field": "custom_form_data__d_063",
                "title": "35 - Date du Bilan de consommation",
                "fct": "date",
                "arg": "%Y-%m-%d",
            },
            {
                "field": "custom_form_data__d_065",
                "title": "36 - Date du test d'étanchéité à l'air",
                "fct": "date",
                "arg": "%Y-%m-%d",
            },
            {
                "field": "custom_form_data__d_067",
                "title": "37 - Date de Prise en main finale",
                "fct": "date",
                "arg": "%Y-%m-%d",
            },
            {
                "field": "updated_at",
                "title": "38 - Date mise à jour Technique",
                "fct": "date",
                "arg": "%Y-%m-%d",
            },
            {
                "field": "linked_object__inseecode",
                "title": "39 - Code Insee",
                "fct": "nop",
            },
        ]

        return columns

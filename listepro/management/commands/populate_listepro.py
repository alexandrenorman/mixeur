"""
Ce script permet de générer le référentiel de base pour listepro

Pour le lancer :

    inv run -c "populate_listepro"

S'il rencontre un problème à l'exécution, rien ne sera créé.

"""

from django.core.management.base import BaseCommand
from django.db import transaction

from listepro.models import (
    Activity,
    CalculationMethod,
    Job,
    KeyWord,
    KeyWordCategory,
    Mission,
    Segment,
    SubMission,
    UsageIntegrated,
)


class Command(BaseCommand):
    help = "Create models for Listepro organizations"  # NOQA: A003

    @transaction.atomic  # NOQA: CFQ001
    def handle(self, *args, **options):

        print("Creating segments…")
        renovation, construction_neuve = map_first(
            [
                Segment.objects.get_or_create(
                    name=name,
                )
                for name in ["Rénovation", "Construction neuve"]
            ]
        )

        print("Creating missions...")
        (
            audit,
            maitrise_oeuvre,
            accompagnement,
            financement,
            execution_travaux,
        ) = map_first(
            [
                Mission.objects.get_or_create(
                    name=name,
                    help_text=help_text,
                )
                for name, help_text in [
                    (
                        "Audit",
                        """Vous souhaitez réaliser un premier état des lieux de votre bâtiment et de ses équipements pour
                     avoir une meilleure idée des travaux envisageables avec des éléments chiffrés (gains énergétique,
                     coûts) et vous aider dans la définition d’un programme de travaux. Vous souhaitez réaliser un
                     autre type de diagnostic dans votre bâtiment.""",
                    ),
                    (
                        "Maitrise d'oeuvre",
                        """Vous avez défini un programme de travaux et vous souhaitez réaliser des études détaillées dans
                     l’objectif de consulter ensuite des entreprises de travaux. La maîtrise d’œuvre englobe des phases
                     de conception et préconisations, allant jusqu’au suivi éventuel des travaux. Un maître d’œuvre peut
                     être un architecte, un bureau d’études, un économiste, un prestataire généraliste, une entreprise
                      générale. Un maître d’œuvre engage sa responsabilité dans les travaux qui seront réalisés.""",
                    ),
                    (
                        "Accompagnement",
                        """Vous souhaitez être accompagné et conseillé sur un sujet spécifique. L’accompagnateur ne fait pas
                     partie de l’équipe de maîtrise d’œuvre du projet. C’est un tiers indépendant qui n’engage pas sa
                     responsabilité sur les travaux réalisés.""",
                    ),
                    (
                        "Financement",
                        """Vous souhaitez financer ou trouver des sources de financement pour la réalisation de votre
                         projet.""",
                    ),
                    (
                        "Exécution travaux",
                        """Vous souhaitez réaliser des travaux avec des entreprises de travaux regroupées sous forme
                         de groupements pour vous proposer une offre globale. Les groupements recensés ici peuvent être
                         des groupements formels, des sociétés proposant de la contractance générale. ils assurent la
                         conception, la coordination et la réalisation de votre projet.""",
                    ),
                ]
            ]
        )

        print("Creating submissions...")
        (
            audit_global,
            audit_energetique,
            diagnostic_technique_global,
            sante_batiment,
            calcul_thermique_reglementaire,
            offre_globale,
            chauffage_ventilation_climatisation,
            bati_architecture,
            accompagnateur_copropriete,
            syndic,
            ingenierie_financiere,
            habitat_participatif,
            assistance_maitrise_usage,
            negociation_contrat_exploitation_fourniture,
            banques,
            banques_pret_copropriete,
            surelevation,
            constructeur_maison,
            offre_globale_travaux,
        ) = map_first(
            [
                SubMission.objects.get_or_create(
                    name=name, help_text=help_text, mission=mission
                )
                for name, mission, help_text in [
                    (
                        "audit global (architectural et energétique)",
                        audit,
                        """<p>Vous souhaitez réaliser un audit énergétique qui prenne en compte la dimension
                         architecturale car : </p><ul><li>votre bâtiment a des caractéristiques architecturales
                         notables (bâti ancien, patrimoine 20°siècle…)</li><li>Vous envisagez une extension
                         </li><li>Vous souhaitez intégrer en amont la faisabilité réglementaire du projet au
                          regard des règles d’urbanisme</li></ul>""",
                    ),
                    (
                        "audit énergétique",
                        audit,
                        """<p>Vous envisagez une rénovation globale, vous souhaitez avoir un état des lieux
                         de votre bâtiment et de vos équipements, et étudier différents scénarios de travaux.
                         <br> Vous avez besoin d’effectuer des choix techniques au regard d’une performance
                          énergétique visée ou d’un niveau de confort à atteindre. <br> Vous avez besoin
                          d’éléments chiffrés (préconisations de travaux, gains énergétiques, montants des
                           travaux) pour vous aider à définir votre programme de travaux.</p>""",
                    ),
                    (
                        "diagnostic technique global (DTG)",
                        audit,
                        """Dans votre copropriété vous cherchez à réaliser un diagnostic intégrant un audit
                         énergétique et une analyse des besoins d'entretien et remise aux normes du bâtiment""",
                    ),
                    (
                        "santé dans le bâtiment",
                        audit,
                        """Vous souhaitez réaliser un audit sur des paramètres déterminant pour la santé
                         dans le bâtiment (qualité de l’air intérieur, lumière, acoustique…)""",
                    ),
                    (
                        "calcul thermique réglementaire",
                        maitrise_oeuvre,
                        """<p>Réglementaire : Vous avez besoin d’une étude thermique pour déposer un permis
                         de construire ou un dossier de subvention</p><p>De dimensionnement : Vous avez
                         besoin de dimensionner des équipements de production de chaleur et/ ou d’eau
                         chaude sanitaire, de climatisation, de ventilation  </p>""",
                    ),
                    (
                        "offre globale (CVC et bâti)",
                        maitrise_oeuvre,
                        """Vous cherchez un maître d'oeuvre réalisant des études sur les lots chauffage
                         / ventilation / climatisation et bâti / architecture""",
                    ),
                    (
                        "chauffage/ventilation/climatisation",
                        maitrise_oeuvre,
                        """Vous cherchez à réaliser des travaux portant sur les systèmes énergétiques
                         du bâtiment. Vous avez besoin de dimensionner des équipements de production
                          de chaleur et/ ou d’eau chaude sanitaire, de climatisation, de ventilation""",
                    ),
                    (
                        "bâti et architecture",
                        maitrise_oeuvre,
                        """Vous cherchez à réaliser des travaux portant sur l’enveloppe du bâtiment""",
                    ),
                    (
                        "accompagnateur copropriété",
                        accompagnement,
                        """Dans le cadre de la rénovation de votre copropriété, vous souhaitez être appuyé
                         dans l’animation de réunion, l'organisation de la communication du projet, la
                         sensibilisation des copropriétaires, la vérification des situations des copropriétaires
                         pour l’éligibilité à des aides financières individuelles. L’accompagnateur copropriété
                         s’apparente à un assistant maîtrise d’ouvrage et ne fait pas partie de l’équipe
                         de maîtrise d’œuvre en place sur le projet.""",
                    ),
                    (
                        "syndic",
                        accompagnement,
                        """Vous cherchez un syndic formé par l’Espace Info Energie du Rhône et de la métropole
                         de Lyon sur les sujets de rénovation énergétique en copropriété""",
                    ),
                    (
                        "ingéniérie financière",
                        accompagnement,
                        """Dans le cadre de la rénovation de votre copropriété, vous cherchez à réaliser un
                         calcul des quotes-parts en déduisant les aides financières et en prenant en compte
                         les économies de charges du projet.""",
                    ),
                    (
                        "habitat participatif",
                        accompagnement,
                        """Vous souhaitez monter un projet d’habitat participatif et cherchez à être accompagné
                         sur le montage juridique, financier de l’opération""",
                    ),
                    (
                        "assistance maîtrise d’usage",
                        accompagnement,
                        """Vous souhaitez être conseillé et mettre en œuvre des actions spécifiques sur les
                         eco-gestes, la maîtrise de vos usages dans votre habitation, votre copropriété, vos
                         locaux tertiaires""",
                    ),
                    (
                        "negociation contrat exploitation fourniture",
                        accompagnement,
                        """Vous avez réalisé des travaux énergétiques et souhaitez être aidé pour réévaluer
                         vos besoins et renégocier votre contrat de chauffage""",
                    ),
                    (
                        "banques",
                        financement,
                        """Vous souhaitez obtenir un prêt pour vos travaux avec des banques sensibilisées
                         sur l’intérêt de la rénovation, sur les dispositifs d’aides financières et leur
                         intégration à votre projet de financement""",
                    ),
                    (
                        "banques prêt copropriété",
                        financement,
                        """Vous souhaitez proposer un prêt collectif dans le cadre des travaux de rénovation
                         de votre copropriété""",
                    ),
                    (
                        "surélévation",
                        financement,
                        """Vous souhaitez évaluer le potentiel de surélévation de votre bâtiment et être
                         accompagné sur le montage de ce type d’opérations""",
                    ),
                    (
                        "constructeur maison",
                        financement,
                        """Vous souhaitez faire appel à un constructeur de maison pour votre projet neuf.""",
                    ),
                    (
                        "offre globale travaux",
                        financement,
                        """Vous souhaitez faire appel à une offre globale et coordonnée pour la rénovation
                         énergétique performante de votre logement.""",
                    ),
                ]
            ]
        )

        print("Creating activities...")
        maison, petit_collectif, copropriété, tertiaire = map_first(
            [
                Activity.objects.get_or_create(
                    name=name,
                )
                for name in ["maison", "petit collectif", "copropriété", "tertiaire"]
            ]
        )

        print("Creating jobs...")
        (
            architecte,
            economistes,
            constructeurs,
            accompagnateur_copro,
            syndic,
            assistant_maitrise_usage,
            accompagnateur_habitat_groupe,
            banques,
            promoteur_surélévation,
            groupement_entreprises,
            contractant_général,
            bureau_etudes,
            maitre_oeuvre,
        ) = map_first(
            [
                Job.objects.get_or_create(
                    name=name,
                )
                for name in [
                    "architecte",
                    "Economistes",
                    "Constructeurs",
                    "Accompagnateur copro",
                    "Syndic",
                    "Assistant à maîtrise d’usage",
                    "Accompagnateur habitat groupé",
                    "Banques",
                    "Promoteur en surélévation",
                    "Groupement d’entreprises",
                    "Contractant général",
                    "Bureau d'études",
                    "Maître d'oeuvre",
                ]
            ]
        )

        print("Creating methods of calculation...")
        (
            statique_THCEEX,
            statique_THBCE,
            statique_PHPP,
            statique_comportemental,
            reelle,
            dynamique,
        ) = map_first(
            [
                CalculationMethod.objects.get_or_create(
                    name=name,
                )
                for name in [
                    "Simulation Thermique Statique (THCE EX)",
                    "Simulation Thermique Statique (TH BCE)",
                    "Simulation Thermique Statique (PHPP)",
                    "Simulation Thermique Statique (Comportementale)",
                    "Réelle (sur factures/mesures)",
                    "Simulation Thermique Dynamique",
                ]
            ]
        )

        print("Creating usages integrated...")
        (
            chauffage,
            refroidissement,
            auxiliaire,
            eclairage,
            electricite_specifique,
            eau_chaude_sanitaire,
        ) = map_first(
            [
                UsageIntegrated.objects.get_or_create(
                    name=name,
                )
                for name in [
                    "Chauffage",
                    "Refroidissement",
                    "Auxiliaire",
                    "Éclairage",
                    "Electricité spécifique",
                    "Eau chaude sanitaire",
                ]
            ]
        )

        print("Creating categories of key words...")
        (
            conception,
            materiaux,
            conceptions_techniques,
            mesures_gestion,
            label_certif,
            accompagnement,
            financement,
            execution_travaux,
        ) = map_first(
            [
                KeyWordCategory.objects.get_or_create(
                    name=name,
                )
                for name in [
                    "Conception",
                    "Matériaux",
                    "Conceptions techniques",
                    "Mesures et Gestion",
                    "Label, certif",
                    "Accompagnement",
                    "Financement",
                    "Exécution travaux",
                ]
            ]
        )

        print("Creating key words...")
        (
            infiltrometrie_etancheite,
            pret_collectif,
            ingenierie_financiere,
            plomberie_chauffage,
            effinergie,
            ACV_energie_grise,
            paille,
            patrimoine,
            plomberie_sanitaire,
            paysage,
            financement,
            animation_reunion,
            passivhaus,
            commissionnement_energetique,
            electricite,
            construction_bois,
            promotion_immobilière,
            communication_copropriete,
            electricite_generale,
            BEPOS,
            exploitation_maintenance,
            photovoltaique,
            construction_terre,
            urbanisme,
            platrerie_peinture,
            surelevation,
            assistance_juridique,
            EC,
            contrat_performance_energetiq,
            solaire_thermique,
            materiaux_biosources,
            bati_ancien,
            conduite_projet,
            charpente,
            BBC_renovation,
            assistance_maitrise_ouvrage,
            bois_energie,
            amiante,
            surelevation,
            ossature_bois,
            MINERGIE,
            recuperation_chaleur,
            dossier_ANAH,
            gestion_humidite,
            extension,
            suivi_consos,
            recuperation_eaux_pluie,
            montage_projet_renovation,
            isolation_thermique_exterieur,
            HQE,
            suivis_chantier,
            pompe_chaleur,
            sobriete_energetique,
            isolation_thermique_interieur,
            LEED,
            BIM,
            ecogestes,
            bardage,
            BREEAM,
            qualite_air_interieur,
            démarche_participative,
            isolation_toiture,
            DPE,
            isolation_combles,
            co_construction,
            audit_energetique,
            assistance_maitrise_usages,
            flocage_thermique,
            diagnostic_technique_global,
            ventilation,
            chauffage_ventilation_climat,
            menuiseries,
            reseau_chauffage_urbain,
            enduit_façade,
            reseau_chaleur,
            energies_renouvelables,
            simulation_thermique_dynamique,
            etancheité_air,
            legionellose,
            structure,
            suivi_chantier,
            RGE_études,
        ) = map_first(
            [
                KeyWord.objects.get_or_create(name=name, category=category)
                for name, category in [
                    ("infiltrométrie, test étanchéité", mesures_gestion),
                    ("prêt collectif", financement),
                    ("ingénierie financière", accompagnement),
                    ("plomberie - chauffage", execution_travaux),
                    ("Effinergie", label_certif),
                    ("ACV, énergie grise", conceptions_techniques),
                    ("paille", materiaux),
                    ("patrimoine", conception),
                    ("plomberie - sanitaire", execution_travaux),
                    ("paysage", conception),
                    ("financement", financement),
                    ("animation de reunion", accompagnement),
                    ("Passivhaus", label_certif),
                    ("commissionnement énergétique", mesures_gestion),
                    ("électricité", conceptions_techniques),
                    ("construction bois", materiaux),
                    ("promotion immobilière", financement),
                    ("communication en copropriété", accompagnement),
                    ("électricité générale", execution_travaux),
                    ("BEPOS", label_certif),
                    ("exploitation maintenance", mesures_gestion),
                    ("photovoltaïque", conceptions_techniques),
                    ("construction terre", materiaux),
                    ("urbanisme", conception),
                    ("plâtrerie - peinture", execution_travaux),
                    ("surélévation", financement),
                    ("assistance juridique", accompagnement),
                    ("E+C-", label_certif),
                    ("contrat de performance énergétiq", mesures_gestion),
                    ("solaire thermique", conceptions_techniques),
                    ("matériaux biosourcés", materiaux),
                    ("bâti ancien", conception),
                    ("conduite de projet", accompagnement),
                    ("charpente", execution_travaux),
                    ("BBC rénovation", label_certif),
                    ("assistance à maîtrise d'ouvrage", mesures_gestion),
                    ("bois energie", conceptions_techniques),
                    ("amiante", materiaux),
                    ("surélévation", conception),
                    ("ossature bois", execution_travaux),
                    ("MINERGIE", label_certif),
                    ("récupération de chaleur", conceptions_techniques),
                    ("dossier ANAH", accompagnement),
                    ("gestion de l'humidité", mesures_gestion),
                    ("extension", conception),
                    ("suivi des consos", mesures_gestion),
                    ("récupération des eaux de pluie", conceptions_techniques),
                    ("montage de projet de rénovation", accompagnement),
                    ("isolation thermique extérieur", execution_travaux),
                    ("HQE", label_certif),
                    ("suivis de chantier", conception),
                    ("pompe à chaleur", conceptions_techniques),
                    ("sobriété énergétique", accompagnement),
                    ("isolation thermique intérieur", execution_travaux),
                    ("LEED", label_certif),
                    ("BIM (Maquette numérique)", conception),
                    ("ecogestes", accompagnement),
                    ("bardage", execution_travaux),
                    ("BREEAM", label_certif),
                    ("qualité de l'air intérieur (QAI)", conceptions_techniques),
                    ("démarche participative", accompagnement),
                    ("isolation toiture", execution_travaux),
                    ("DPE", conceptions_techniques),
                    ("isolation combles", execution_travaux),
                    ("co-construction", accompagnement),
                    ("audit énergétique", conceptions_techniques),
                    ("assistance à maîtrise d'usages", accompagnement),
                    ("flocage thermique", execution_travaux),
                    ("diagnostic technique global", conceptions_techniques),
                    ("ventilation", execution_travaux),
                    ("chauffage/ventilation/climat.", conceptions_techniques),
                    ("menuiseries", execution_travaux),
                    ("Réseau de chauffage urbain", conceptions_techniques),
                    ("enduit de façade", execution_travaux),
                    ("réseau de chaleur", conceptions_techniques),
                    ("Energies Renouvelables", conceptions_techniques),
                    ("simulation thermique dynamique", conceptions_techniques),
                    ("etanchéité à l'air", conceptions_techniques),
                    ("légionellose", conceptions_techniques),
                    ("structure", conceptions_techniques),
                    ("suivi de chantier", conceptions_techniques),
                    ("RGE études", conceptions_techniques),
                ]
            ]
        )

    print("Everything has been created, Listepro is ready")


def map_first(list_of_tuples):
    return [first for first, _ in list_of_tuples]

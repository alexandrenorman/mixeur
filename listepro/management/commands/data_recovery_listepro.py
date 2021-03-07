"""
Ce script permet de gérer la reprise de donées pour listepro

Pour le lancer :

    inv run -c "data_recovery_listepro"

S'il rencontre un problème à l'exécution, rien ne sera créé.

"""
import json
from urllib.parse import urlparse

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.db import transaction

import requests

from accounts.models import User

from listepro.models import (
    Activity,
    CalculationMethod,
    Job,
    KeyWord,
    KeyWordCategory,
    Mission,
    Professional,
    ProfessionalImage,
    ProfessionalProduction,
    Segment,
    SegmentActivitySubMissionLink,
    SubMission,
    UsageIntegrated,
)


_OLD_IMAGE_PATH = "https://www.professionnels-info-energie-69.org/media/"


def _delete_all_professionals():
    models = [
        ProfessionalImage,
        ProfessionalProduction,
        Professional,
        SegmentActivitySubMissionLink,
        Job,
        Segment,
        Activity,
        KeyWordCategory,
        KeyWord,
        SubMission,
        Mission,
        CalculationMethod,
        UsageIntegrated,
    ]
    for item in models:
        item.objects.all().delete()


class Command(BaseCommand):
    help = "Manage data recovery from old datas"  # NOQA: A003

    @transaction.atomic  # NOQA: CFQ001, C901
    def handle(self, *args, **options):

        file = "media/listepro/professionals_reprise.json"
        try:
            json_data = open(file)
        except FileNotFoundError:
            print(f"Le fichier {file} est introuvable")
            return
        data = json.load(json_data)

        _delete_all_professionals()
        # MISSION
        mission_map = {}
        for old_mission in data:
            if old_mission["model"] == "professionals.mission":
                kwargs = old_mission["fields"]
                name = kwargs.pop("name")
                mission, _created = Mission.objects.update_or_create(
                    name=name,
                    defaults=kwargs,
                )
                mission_map[old_mission["pk"]] = mission

        # SUBMISSION
        sub_mission_map = {}
        for old_sub_mission in data:
            if old_sub_mission["model"] == "professionals.submission":
                kwargs = old_sub_mission["fields"]
                name = kwargs.pop("name")
                kwargs["mission"] = mission_map[kwargs["mission"]]
                sub_mission, _created = SubMission.objects.update_or_create(
                    name=name,
                    defaults=kwargs,
                )
                sub_mission_map[old_sub_mission["pk"]] = sub_mission

        # KEYWORDCATEGORY
        keyword_category_map = {}
        for old_keyword_category in data:
            if old_keyword_category["model"] == "professionals.keywordcategory":
                kwargs = old_keyword_category["fields"]
                name = kwargs.pop("name")
                keyword_category, _created = KeyWordCategory.objects.update_or_create(
                    name=name,
                    defaults=kwargs,
                )
                keyword_category_map[old_keyword_category["pk"]] = keyword_category

        # KEYWORD
        keyword_map = {}
        for old_keyword in data:
            if old_keyword["model"] == "professionals.keyword":
                kwargs = old_keyword["fields"]
                name = kwargs.pop("name")
                category = keyword_category_map[kwargs.pop("category")]
                print(f"Mot clé: {name}")
                keyword, _created = KeyWord.objects.update_or_create(
                    name=name,
                    category=category,
                    defaults=kwargs,
                )
                keyword_map[old_keyword["pk"]] = keyword

        # ACTIVITY
        activity_map = {}
        for old_activity in data:
            if old_activity["model"] == "professionals.activity":
                kwargs = old_activity["fields"]
                name = kwargs.pop("name")
                activity, _created = Activity.objects.update_or_create(
                    name=name,
                    defaults=kwargs,
                )
                activity_map[old_activity["pk"]] = activity

        # JOB
        job_map = {}
        for old_job in data:
            if old_job["model"] == "professionals.job":
                kwargs = old_job["fields"]
                name = kwargs.pop("name")
                job, _created = Job.objects.update_or_create(
                    name=name,
                    defaults=kwargs,
                )
                job_map[old_job["pk"]] = job

        # SEGMENT
        segment_map = {}
        for old_segment in data:
            if old_segment["model"] == "professionals.segment":
                kwargs = old_segment["fields"]
                name = kwargs.pop("name")
                segment, _created = Segment.objects.update_or_create(
                    name=name,
                    defaults=kwargs,
                )
                segment_map[old_segment["pk"]] = segment

        # SEGMENTACTIVITYSUBMISSIONLINK
        for old_segment_activity_submission_link in data:
            if (
                old_segment_activity_submission_link["model"]
                == "professionals.segmentactivitysubmissionlink"
            ):
                kwargs = old_segment_activity_submission_link["fields"]
                kwargs["segment"] = segment_map[kwargs["segment"]]
                kwargs["activity"] = activity_map[kwargs["activity"]]
                kwargs["sub_mission"] = sub_mission_map[kwargs["sub_mission"]]

                (
                    segment_activity_submission_link,
                    _created,
                ) = SegmentActivitySubMissionLink.objects.get_or_create(
                    **kwargs,
                )

        # CALCULATIONMETHOD
        calculation_method_map = {}
        for old_calculation_method in data:
            if old_calculation_method["model"] == "professionals.calculationmethod":
                kwargs = old_calculation_method["fields"]
                name = kwargs.pop("name")
                (
                    calculation_method,
                    _created,
                ) = CalculationMethod.objects.update_or_create(
                    name=name,
                    defaults=kwargs,
                )
                calculation_method_map[
                    old_calculation_method["pk"]
                ] = calculation_method

        # USAGEINTEGRATED
        usage_integrated_map = {}
        for old_usage_integrated in data:
            if old_usage_integrated["model"] == "professionals.usageintegrated":
                kwargs = old_usage_integrated["fields"]
                name = kwargs.pop("name")
                usage_integrated, _created = UsageIntegrated.objects.update_or_create(
                    name=name,
                    defaults=kwargs,
                )
                usage_integrated_map[old_usage_integrated["pk"]] = usage_integrated

        # user
        user_map = {}
        for old_user in data:
            if old_user["model"] == "accounts.user":
                kwargs = old_user["fields"]
                email = kwargs.pop("email")
                kwargs["last_name"] = kwargs.pop("fullname")
                kwargs["civility"] = (
                    kwargs["civility"] if kwargs["civility"] is not None else ""
                )
                if not kwargs["is_staff"]:
                    kwargs["user_type"] = "professional"
                kwargs.pop("primary_group")
                kwargs.pop("groups")
                kwargs.pop("user_permissions")
                user, _created = User.objects.get_or_create(
                    email=email,
                    defaults=kwargs,
                )
                user_map[old_user["pk"]] = user

        # PROFESSIONNAL
        professional_map = {}
        for old_professional in data:
            if old_professional["model"] == "professionals.professional":
                kwargs = old_professional["fields"]
                name = kwargs.pop("name")
                user = user_map[kwargs.pop("user")]
                # GEOM
                old_geom = json.loads(json.loads(kwargs.pop("geom")))
                new_geom = {
                    "lat": old_geom["coordinates"][1],
                    "lon": old_geom["coordinates"][0],
                }

                kwargs["geom"] = new_geom

                #  LOGO
                logo_pk = kwargs.pop("logo")

                # MODIFIED FIELD NAME
                kwargs["created_at"] = kwargs.pop("date_created")
                kwargs["updated_at"] = kwargs.pop("date_modified")
                kwargs["pro_is_valid"] = kwargs.pop("is_valid")
                # DELETE FIELD
                kwargs.pop("short_description")
                # MAPPED FIELD
                kwargs["job"] = job_map[kwargs["job"]]
                kwargs["activity_first"] = activity_map[kwargs["activity_first"]]
                kwargs["activity_second"] = (
                    activity_map[kwargs["activity_second"]]
                    if kwargs["activity_second"]
                    else None
                )
                kwargs["activity_third"] = (
                    activity_map[kwargs["activity_third"]]
                    if kwargs["activity_third"]
                    else None
                )
                kwargs["activity_fourth"] = (
                    activity_map[kwargs["activity_fourth"]]
                    if kwargs["activity_fourth"]
                    else None
                )
                # M2M FIELD
                segments = [segment_map[i] for i in kwargs.pop("segments")]
                primary_key_words = [
                    keyword_map[i] for i in kwargs.pop("primary_key_words")
                ]
                secondary_key_words = [
                    keyword_map[i] for i in kwargs.pop("secondary_key_words")
                ]
                sub_missions = [sub_mission_map[i] for i in kwargs.pop("sub_missions")]
                print(f"Professionel : {name}")
                professional, _created = Professional.objects.update_or_create(
                    name=name,
                    user=user,
                    defaults=kwargs,
                )

                # M2M FIELD
                professional.segments.set(segments)
                professional.primary_key_words.set(primary_key_words)
                professional.secondary_key_words.set(secondary_key_words)
                professional.sub_missions.set(sub_missions)
                professional_map[old_professional["pk"]] = professional

                #  LOGO
                if logo_pk:
                    logo_url = (
                        _OLD_IMAGE_PATH
                        + [
                            i["fields"]["cropped"]
                            for i in data
                            if (
                                i["model"] == "professionals.professionalimage"
                                and i["pk"] == logo_pk
                            )
                        ][0]
                    )

                    logo_name = urlparse(logo_url).path.split("/")[-1]

                    response = requests.get(logo_url)
                    if response.status_code == 200:
                        professional.logo.save(
                            logo_name, ContentFile(response.content), save=True
                        )

        # PROFESSIONNAL PRODUCTION
        professional_production_map = {}
        for old_professional_production in data:
            if (
                old_professional_production["model"]
                == "professionals.professionalproduction"
            ):
                kwargs = old_professional_production["fields"].copy()
                production_name = kwargs.pop("production_name")
                professional = professional_map[kwargs.pop("professional")]

                kwargs["label"] = kwargs["label"] if kwargs["label"] is not None else ""

                # MODIFIED FIELD NAME
                kwargs["created_at"] = kwargs.pop("date_created")
                kwargs["updated_at"] = kwargs.pop("date_modified")
                # DELETE FIELD
                # TODO: manage image
                kwargs.pop("pictures")
                # MAPPED FIELD
                kwargs["calculation_method"] = (
                    calculation_method_map[kwargs["calculation_method"]]
                    if kwargs["calculation_method"]
                    else None
                )
                # M2M FIELD
                usage_integrated = [
                    usage_integrated_map[i] for i in kwargs.pop("usage_integrated")
                ]

                (
                    professional_production,
                    _created,
                ) = ProfessionalProduction.objects.update_or_create(
                    production_name=production_name,
                    professional=professional,
                    defaults=kwargs,
                )

                # M2M FIELD
                professional_production.usage_integrated.set(usage_integrated)

                professional_production_map[
                    old_professional_production["pk"]
                ] = professional_production

                # MANAGE IMAGE
                pictures_data = [
                    i
                    for i in data
                    if (
                        i["model"] == "professionals.professionalimage"
                        and i["pk"] in old_professional_production["fields"]["pictures"]
                    )
                ]
                for old_professional_image in pictures_data:
                    kwargs = old_professional_image["fields"]
                    (
                        professional_image,
                        _created,
                    ) = ProfessionalImage.objects.update_or_create(
                        name=kwargs[("name")], production=professional_production
                    )
                    logo_url = _OLD_IMAGE_PATH + kwargs[("cropped")]

                    logo_name = urlparse(logo_url).path.split("/")[-1]

                    response = requests.get(logo_url)
                    if response.status_code == 200:
                        professional_image.cropped.save(
                            logo_name, ContentFile(response.content), save=True
                        )
                        professional_image.save()

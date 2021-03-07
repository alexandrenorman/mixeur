# -*- coding: utf-8 -*-
import csv
import io


class ExperienceCSVSerializer:
    def __init__(self, experiences, *args, **kwargs):
        self.experiences = experiences

    @property
    def data(self):
        csv_fh = io.StringIO()
        # delimiter=";" because excel.
        csv_writer = csv.writer(csv_fh, delimiter=";", quoting=csv.QUOTE_ALL)
        csv_writer.writerow(
            [
                # https://en.wikipedia.org/wiki/Byte_order_mark
                "\ufeffNom",
                "Projet vitrine",
                "Référence interne",
                "Pilote de projet",
                "Années",
                "Financeurs",
                "Métiers",
                "Publics",
                "Missions",
                "Tags",
                "Durée de réalisation (en jours)",
                "Budget total (en €)",
                "Budget de la structure (en €)",
                "Partenaires",
                "Description",
                "Description (en anglais)",
                "Rôle de la structure",
                "Site web",
                "Image 1",
                "Image 2",
            ]
        )

        url = ""
        for experience in self.experiences:
            csv_writer.writerow(
                [
                    experience.title,
                    "X" if experience.is_showcase else "",
                    experience.internal_reference,
                    experience.referent.full_name,
                    ", ".join([x.name for x in experience.years.all()]),
                    "\n".join(
                        [
                            ", ".join(
                                [
                                    x.sponsor.name,
                                    x.title if x.title else "-",
                                    x.contract_number if x.contract_number else "-",
                                ]
                            )
                            for x in experience.sponsors.all()
                        ]
                    ),
                    ", ".join([x.name for x in experience.jobs.all()]),
                    ", ".join([x.name for x in experience.publics.all()]),
                    ", ".join([x.name for x in experience.assignments.all()]),
                    ", ".join([x.name for x in experience.tags.all()]),
                    experience.duration,
                    experience.budget,
                    experience.budget_group,
                    ", ".join([x.name for x in experience.partners.all()]),
                    experience.description_as_ascii,
                    experience.description_en_as_ascii,
                    experience.role_as_ascii,
                    experience.url,
                    (url + experience.image1.url) if experience.image1 else "",
                    (url + experience.image2.url) if experience.image2 else "",
                ]
            )
        csv_fh.seek(0)
        return {"csv": csv_fh.read()}

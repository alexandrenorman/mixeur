# Generated by Django 2.2.3 on 2019-10-24 14:28

import core.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("accounts", "0003_auto_20191003_1408"),
        ("fac", "0017_auto_20191021_1022"),
    ]

    operations = [
        migrations.CreateModel(
            name="Tag",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        default=django.utils.timezone.now, editable=False
                    ),
                ),
                (
                    "updated_at",
                    core.models.AutoDateTimeField(
                        default=django.utils.timezone.now, editable=False
                    ),
                ),
                (
                    "name",
                    models.CharField(max_length=100, unique=True, verbose_name="Name"),
                ),
                (
                    "description",
                    models.CharField(
                        blank=True, max_length=100, null=True, verbose_name="Description"
                    ),
                ),
                (
                    "slug",
                    models.SlugField(blank=True, max_length=100, null=True, unique=True),
                ),
                (
                    "owning_group",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="tags",
                        to="accounts.Group",
                        verbose_name="Groupe propri??taire",
                    ),
                ),
            ],
            options={"abstract": False},
        ),
        migrations.AlterUniqueTogether(name="filetag", unique_together=None),
        migrations.RemoveField(model_name="filetag", name="owning_group"),
        migrations.AlterUniqueTogether(name="globaltag", unique_together=None),
        migrations.RemoveField(model_name="globaltag", name="owning_group"),
        migrations.DeleteModel(name="Tagulous_MemberOfOrganization_competencies_tags"),
        migrations.RemoveField(model_name="organization", name="referent"),
        migrations.AddField(
            model_name="organization",
            name="referents",
            field=models.ManyToManyField(
                blank=True,
                help_text="Liste de r??f??rents",
                related_name="organization_referents",
                to=settings.AUTH_USER_MODEL,
                verbose_name="R??ferents",
            ),
        ),
        migrations.RemoveField(model_name="contact", name="tags"),
        migrations.RemoveField(model_name="filecontact", name="tags"),
        migrations.RemoveField(model_name="fileorganization", name="tags"),
        migrations.RemoveField(model_name="list", name="tags"),
        migrations.RemoveField(
            model_name="memberoforganization", name="competencies_tags"
        ),
        migrations.RemoveField(model_name="memberoforganization", name="tags"),
        migrations.RemoveField(model_name="notecontact", name="tags"),
        migrations.RemoveField(model_name="noteorganization", name="tags"),
        migrations.RemoveField(model_name="organization", name="tags"),
        migrations.AddField(
            model_name="contact",
            name="tags",
            field=models.ManyToManyField(
                blank=True,
                help_text="Liste de tags",
                related_name="contacts",
                to="fac.Tag",
                verbose_name="Tags",
            ),
        ),
        migrations.AddField(
            model_name="filecontact",
            name="tags",
            field=models.ManyToManyField(
                blank=True,
                help_text="Liste de tags",
                related_name="contact_files",
                to="fac.Tag",
                verbose_name="Tags",
            ),
        ),
        migrations.AddField(
            model_name="fileorganization",
            name="tags",
            field=models.ManyToManyField(
                blank=True,
                help_text="Liste de tags",
                related_name="organization_files",
                to="fac.Tag",
                verbose_name="Tags",
            ),
        ),
        migrations.AddField(
            model_name="list",
            name="tags",
            field=models.ManyToManyField(
                blank=True,
                help_text="l'ensemble des contacts taggu??s avec ces tags seront inclus dans la liste de diffusion",
                related_name="lists",
                to="fac.Tag",
                verbose_name="Tags",
            ),
        ),
        migrations.AddField(
            model_name="memberoforganization",
            name="competencies_tags",
            field=models.ManyToManyField(
                blank=True,
                help_text="Liste de comp??tences",
                related_name="competencies_of_member_of_organization",
                to="fac.Tag",
                verbose_name="Domaine de comp??tences / d'activit??s",
            ),
        ),
        migrations.AddField(
            model_name="memberoforganization",
            name="tags",
            field=models.ManyToManyField(
                blank=True,
                help_text="Liste de tags",
                related_name="functions_of_member_of_organization",
                to="fac.Tag",
                verbose_name="Fonction dans l'organisation (tag)",
            ),
        ),
        migrations.AddField(
            model_name="notecontact",
            name="tags",
            field=models.ManyToManyField(
                blank=True,
                help_text="Liste de tags",
                related_name="contact_notes",
                to="fac.Tag",
                verbose_name="Tags",
            ),
        ),
        migrations.AddField(
            model_name="noteorganization",
            name="tags",
            field=models.ManyToManyField(
                blank=True,
                help_text="Liste de tags",
                related_name="organization_notes",
                to="fac.Tag",
                verbose_name="Tags",
            ),
        ),
        migrations.AddField(
            model_name="organization",
            name="tags",
            field=models.ManyToManyField(
                blank=True,
                help_text="Liste de tags",
                related_name="organizations",
                to="fac.Tag",
                verbose_name="Tags",
            ),
        ),
        migrations.DeleteModel(name="FileTag"),
        migrations.DeleteModel(name="GlobalTag"),
    ]

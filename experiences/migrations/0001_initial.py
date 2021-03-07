# Generated by Django 2.2.11 on 2020-04-21 20:54

import core.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0011_auto_20200224_1144'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AssignmentTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('updated_at', core.models.AutoDateTimeField(default=django.utils.timezone.now, editable=False)),
                ('name', models.CharField(max_length=100, verbose_name='Nom')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('is_active', models.BooleanField(default=True, help_text='Tag actif ?', verbose_name='active')),
                ('owning_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.Group', verbose_name='Groupe propriétaire')),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
                'unique_together': {('owning_group', 'name')},
            },
        ),
        migrations.CreateModel(
            name='YearTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('updated_at', core.models.AutoDateTimeField(default=django.utils.timezone.now, editable=False)),
                ('name', models.CharField(max_length=100, verbose_name='Nom')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('is_active', models.BooleanField(default=True, help_text='Tag actif ?', verbose_name='active')),
                ('owning_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.Group', verbose_name='Groupe propriétaire')),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
                'unique_together': {('owning_group', 'name')},
            },
        ),
        migrations.CreateModel(
            name='PublicTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('updated_at', core.models.AutoDateTimeField(default=django.utils.timezone.now, editable=False)),
                ('name', models.CharField(max_length=100, verbose_name='Nom')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('is_active', models.BooleanField(default=True, help_text='Tag actif ?', verbose_name='active')),
                ('owning_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.Group', verbose_name='Groupe propriétaire')),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
                'unique_together': {('owning_group', 'name')},
            },
        ),
        migrations.CreateModel(
            name='PartnerTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('updated_at', core.models.AutoDateTimeField(default=django.utils.timezone.now, editable=False)),
                ('name', models.CharField(max_length=100, verbose_name='Nom')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('is_active', models.BooleanField(default=True, help_text='Tag actif ?', verbose_name='active')),
                ('is_european', models.BooleanField(default=False, verbose_name='partenaire européen ?')),
                ('owning_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.Group', verbose_name='Groupe propriétaire')),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
                'unique_together': {('owning_group', 'name')},
            },
        ),
        migrations.CreateModel(
            name='JobTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('updated_at', core.models.AutoDateTimeField(default=django.utils.timezone.now, editable=False)),
                ('name', models.CharField(max_length=100, verbose_name='Nom')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('is_active', models.BooleanField(default=True, help_text='Tag actif ?', verbose_name='active')),
                ('owning_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.Group', verbose_name='Groupe propriétaire')),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
                'unique_together': {('owning_group', 'name')},
            },
        ),
        migrations.CreateModel(
            name='ExperienceTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('updated_at', core.models.AutoDateTimeField(default=django.utils.timezone.now, editable=False)),
                ('name', models.CharField(max_length=100, verbose_name='Nom')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('is_active', models.BooleanField(default=True, help_text='Tag actif ?', verbose_name='active')),
                ('owning_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.Group', verbose_name='Groupe propriétaire')),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
                'unique_together': {('owning_group', 'name')},
            },
        ),
        migrations.CreateModel(
            name='Experience',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('updated_at', core.models.AutoDateTimeField(default=django.utils.timezone.now, editable=False)),
                ('title', models.CharField(max_length=150, verbose_name='Titre')),
                ('description', models.TextField(verbose_name='Description')),
                ('internal_reference', models.CharField(blank=True, max_length=150, null=True, verbose_name='Référence interne')),
                ('image1', models.ImageField(blank=True, null=True, upload_to='', verbose_name='Illustration 1')),
                ('image2', models.ImageField(blank=True, null=True, upload_to='', verbose_name='Illustration 2')),
                ('duration', models.PositiveIntegerField(default=0, verbose_name='Durée de réalisation (en jours)')),
                ('sponsor', models.CharField(blank=True, max_length=150, null=True, verbose_name='Financeur')),
                ('budget', models.FloatField(default=0, verbose_name='Budget total (en €)')),
                ('budget_group', models.FloatField(default=0, verbose_name='Budget de la structure (en €)')),
                ('role', models.TextField(blank=True, null=True, verbose_name='Rôle de la structure')),
                ('description_en', models.TextField(blank=True, null=True, verbose_name='Description (en anglais)')),
                ('url', models.URLField(blank=True, null=True, verbose_name='Site Web')),
                ('assignments', models.ManyToManyField(blank=True, related_name='experience_assignments', to='experiences.AssignmentTag', verbose_name='Missions')),
                ('jobs', models.ManyToManyField(blank=True, related_name='experience_jobs', to='experiences.JobTag', verbose_name='Métiers')),
                ('owning_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='experiences', to='accounts.Group', verbose_name='Groupe propriétaire')),
                ('partners', models.ManyToManyField(blank=True, related_name='experience_partners', to='experiences.PartnerTag', verbose_name='Partenaires')),
                ('publics', models.ManyToManyField(blank=True, related_name='experience_publics', to='experiences.PublicTag', verbose_name='Publics')),
                ('referent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='experiences', to=settings.AUTH_USER_MODEL, verbose_name='Référent')),
                ('tags', models.ManyToManyField(blank=True, related_name='experience_tags', to='experiences.ExperienceTag', verbose_name='Tags')),
                ('years', models.ManyToManyField(blank=True, related_name='experience_years', to='experiences.YearTag', verbose_name='Années')),
            ],
            options={
                'verbose_name': 'Experience',
                'verbose_name_plural': 'Experiences',
            },
        ),
    ]

# Generated by Django 2.2.6 on 2019-11-15 11:30

import core.models
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import newsletters.models.group_of_newsletters
import newsletters.models.image
import newsletters.models.newsletter


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0003_auto_20191003_1408'),
    ]

    operations = [
        migrations.CreateModel(
            name='GroupOfNewsletters',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('updated_at', core.models.AutoDateTimeField(default=django.utils.timezone.now, editable=False)),
                ('slug', models.SlugField(verbose_name='Slug')),
                ('title', models.CharField(max_length=100, verbose_name='Titre')),
                ('is_active', models.BooleanField(default=True, verbose_name='Est publié ?')),
                ('is_public', models.BooleanField(default=True, verbose_name='Est public ?')),
                ('header', models.ImageField(blank=True, null=True, upload_to=newsletters.models.group_of_newsletters.header_path, verbose_name="Image d'entête")),
                ('header_link', models.URLField(blank=True, null=True, verbose_name='Url')),
                ('footer', models.ImageField(blank=True, null=True, upload_to=newsletters.models.group_of_newsletters.footer_path, verbose_name='Image de pied')),
                ('footer_link', models.URLField(blank=True, null=True, verbose_name='Url')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('graphic_charter', django.contrib.postgres.fields.jsonb.JSONField(default=newsletters.models.group_of_newsletters.DEFAULT_GRAPHIC_CHARTER, verbose_name='Charte graphique')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.Group', verbose_name='Structure')),
            ],
            options={
                'verbose_name': 'Groupe de newsletters',
                'unique_together': {('group', 'slug')},
            },
        ),
        migrations.CreateModel(
            name='Newsletter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('updated_at', core.models.AutoDateTimeField(default=django.utils.timezone.now, editable=False)),
                ('slug', models.SlugField(unique='true', verbose_name='Slug')),
                ('title', models.CharField(max_length=100, verbose_name='Titre')),
                ('is_active', models.BooleanField(default=True, verbose_name='Est publiée ?')),
                ('is_public', models.BooleanField(default=True, verbose_name='Est publique ?')),
                ('publication_start_date', models.DateTimeField(auto_now=True, verbose_name='Date et heure de début de publication')),
                ('publication_end_date', models.DateTimeField(blank=True, null=True, verbose_name='Date et heure de fin de publication')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('graphic_charter', django.contrib.postgres.fields.jsonb.JSONField(default=newsletters.models.group_of_newsletters.DEFAULT_GRAPHIC_CHARTER, verbose_name='Charte graphique')),
                ('plugins', django.contrib.postgres.fields.jsonb.JSONField(default=newsletters.models.newsletter.PLUGINS, verbose_name='Liste des plugins')),
                ('group_of_newsletters', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='newsletters.GroupOfNewsletters', verbose_name='Groupe de newsletters')),
            ],
            options={
                'verbose_name': 'Newsletter',
            },
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('updated_at', core.models.AutoDateTimeField(default=django.utils.timezone.now, editable=False)),
                ('image', models.FileField(upload_to=newsletters.models.image.image_directory_path, verbose_name='Document')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='image', to='accounts.Group', verbose_name='Groupe propriétaire')),
            ],
            options={
                'verbose_name': 'Image',
            },
        ),
    ]

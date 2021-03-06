# Generated by Django 2.2.3 on 2019-09-17 14:01

import accounts.models.group
import accounts.models.user
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    replaces = [('accounts', '0001_initial'), ('accounts', '0002_auto_20161206_2259'), ('accounts', '0003_auto_20180302_1049'), ('accounts', '0004_remove_user_username'), ('accounts', '0005_auto_20181121_1602'), ('accounts', '0006_auto_20181125_1757'), ('accounts', '0007_user_profile_pic'), ('accounts', '0008_user_title'), ('accounts', '0009_auto_20190109_1709'), ('accounts', '0010_auto_20190117_1719'), ('accounts', '0011_remove_user_address'), ('accounts', '0012_auto_20190308_2318'), ('accounts', '0013_group_phone'), ('accounts', '0014_user_phone_cache'), ('accounts', '0015_auto_20190527_1010'), ('accounts', '0016_auto_20190527_1015'), ('accounts', '0017_auto_20190607_1129'), ('accounts', '0018_auto_20190607_1640'), ('accounts', '0019_auto_20190618_2210'), ('accounts', '0020_group_email'), ('accounts', '0021_user_color'), ('accounts', '0022_auto_20190726_1526')]

    initial = True

    dependencies = [
        ('territories', '0001_initial'),
        ('white_labelling', '0001_initial'),
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Nom')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('is_active', models.BooleanField(default=True, help_text='Active group ?', verbose_name='active')),
                ('admin_group', models.ForeignKey(blank=True, help_text="Groupe parent qui gère l'administration", null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='managed_groups', to='accounts.Group', verbose_name='Groupe administrateur')),
                ('is_admin', models.BooleanField(default=False, help_text='Groupe utilisé pour gérer les groupes par région ?', verbose_name="Groupe régional d'administration")),
                ('presentation', models.TextField(blank=True, null=True, verbose_name='Présentation de la structure')),
                ('profile_pic', models.ImageField(blank=True, null=True, upload_to=accounts.models.group.group_directory_path)),
                ('territories', models.ManyToManyField(to='territories.Commune', verbose_name='Territoires')),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=100, null=True, region=None, verbose_name='Numéro de téléphone')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='Courriel')),
            ],
            options={
                'verbose_name': 'Groupe',
                'verbose_name_plural': 'Groupes',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('first_name', models.CharField(max_length=300, verbose_name='first name')),
                ('last_name', models.CharField(max_length=300, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='admin ?', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Active user ?', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
                ('civility', models.CharField(blank=True, choices=[('M.', 'M.'), ('Mme', 'Mme'), ('Mlle', 'Mlle')], max_length=8, null=True, verbose_name='civility')),
                ('group', models.ForeignKey(blank=True, help_text="Structure d'appartenance", null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='profile', to='accounts.Group', verbose_name='Groupe')),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=100, null=True, region=None, verbose_name='Numéro de téléphone')),
                ('user_type', models.CharField(choices=[('client', 'Client'), ('advisor', 'Conseiller'), ('manager', 'Responsable'), ('administrator', 'Administrateur')], default='client', max_length=20, verbose_name="Profil d'utilisateur")),
                ('white_labelling', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='profile', to='white_labelling.WhiteLabelling', verbose_name='Domaine / marque blanche')),
                ('profile_pic', models.ImageField(blank=True, null=True, upload_to=accounts.models.user.profile_directory_path)),
                ('title', models.CharField(blank=True, max_length=100, null=True, verbose_name='Titre ou fonction')),
                ('phone_cache', models.CharField(blank=True, max_length=100, null=True, verbose_name='Cache pour le numéro de téléphone')),
                ('color', models.CharField(default='#888888', max_length=10, verbose_name='Color')),
            ],
            options={
                'abstract': False,
                'ordering': ('first_name', 'last_name'),
                'verbose_name': 'Utilisateur',
            },
        ),
        migrations.CreateModel(
            name='RgpdConsent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_date', models.DateTimeField(auto_now_add=True, verbose_name='Date de création')),
                ('allow_to_keep_data', models.BooleanField(default=True, verbose_name='Permettre la conservation de mes données dans le système de traitement.')),
                ('allow_to_use_email_to_send_reminder', models.BooleanField(default=True, verbose_name="Permettre l'utilisation de mon email pour envoyer un rappel de rendez-vous ou des informations liées à mon dossier.")),
                ('allow_to_use_phone_number_to_send_reminder', models.BooleanField(default=True, verbose_name="Permettre l'utilisation de mon numéro de téléphone pour envoyer un rappel de rendez-vous.")),
                ('allow_to_share_my_information_with_my_advisor', models.BooleanField(default=True, verbose_name="Permettre le partage de mes informations avec l'EIE qui suit mon dossier.")),
                ('allow_to_share_my_information_with_partners', models.BooleanField(default=True, verbose_name='Permettre le partage de mes informations avec nos partenaires à des fins statistiques.')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'RgpdConsent',
                'verbose_name_plural': 'RgpdConsents',
                'ordering': ['-creation_date'],
            },
        ),
    ]

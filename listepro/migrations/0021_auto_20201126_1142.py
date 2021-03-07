# Generated by Django 2.2.17 on 2020-11-26 10:42

from django.db import migrations, models
import listepro.models.professional
import listepro.models.professional_image


class Migration(migrations.Migration):

    dependencies = [
        ('listepro', '0020_remove_null'),
    ]

    operations = [
        migrations.AlterField(
            model_name='helper',
            name='help_text',
            field=models.TextField(blank=True, verbose_name="Texte de l'aide"),
        ),
        migrations.AlterField(
            model_name='mission',
            name='help_text',
            field=models.TextField(blank=True, verbose_name="Texte de l'aide"),
        ),
        migrations.AlterField(
            model_name='professional',
            name='comment',
            field=models.TextField(max_length=2000, verbose_name='Commentaire sur le professionnel'),
        ),
        migrations.AlterField(
            model_name='professional',
            name='email',
            field=models.EmailField(blank=True, max_length=254, verbose_name='Email'),
        ),
        migrations.AlterField(
            model_name='professional',
            name='logo',
            field=models.ImageField(blank=True, default=None, upload_to=listepro.models.professional.logo_path),
        ),
        migrations.AlterField(
            model_name='professional',
            name='original_logo',
            field=models.ImageField(blank=True, default=None, upload_to=listepro.models.professional.logo_original_path),
        ),
        migrations.AlterField(
            model_name='professional',
            name='url',
            field=models.URLField(blank=True, verbose_name='Site web'),
        ),
        migrations.AlterField(
            model_name='professionalimage',
            name='cropped',
            field=models.ImageField(blank=True, upload_to=listepro.models.professional_image.img_prof_path),
        ),
        migrations.AlterField(
            model_name='professionalproduction',
            name='airtightness_test_result',
            field=models.CharField(blank=True, max_length=512, verbose_name="Résultat du test d'étanchéité à l'air"),
        ),
        migrations.AlterField(
            model_name='professionalproduction',
            name='label',
            field=models.CharField(blank=True, max_length=256, verbose_name='Label de la réalisation'),
        ),
        migrations.AlterField(
            model_name='professionalproduction',
            name='other_information',
            field=models.CharField(blank=True, max_length=512, verbose_name='Autres informations sur ce projet'),
        ),
        migrations.AlterField(
            model_name='professionalproduction',
            name='system',
            field=models.CharField(blank=True, max_length=512, verbose_name='Système'),
        ),
        migrations.AlterField(
            model_name='professionalproduction',
            name='thermal_envelope',
            field=models.CharField(blank=True, max_length=512, verbose_name='Enveloppe thermique'),
        ),
        migrations.AlterField(
            model_name='submission',
            name='help_text',
            field=models.TextField(blank=True, verbose_name="Texte de l'aide"),
        ),
    ]
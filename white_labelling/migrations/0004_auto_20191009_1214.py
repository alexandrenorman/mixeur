# Generated by Django 2.2.3 on 2019-10-09 10:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('white_labelling', '0003_whitelabelling_site_baseline'),
    ]

    operations = [
        migrations.AddField(
            model_name='whitelabelling',
            name='cee_simul_baseline',
            field=models.CharField(default='Outil de simulation primes CEE', max_length=100, verbose_name="Baseline de l'application Simulateur CEE"),
        ),
        migrations.AddField(
            model_name='whitelabelling',
            name='cee_simul_is_active',
            field=models.BooleanField(default=False, verbose_name='Activer les iframes CEE'),
        ),
        migrations.AddField(
            model_name='whitelabelling',
            name='cee_simul_name',
            field=models.CharField(default='Simulateur CEE', max_length=100, verbose_name="Nom de l'application Simulateur CEE"),
        ),
        migrations.AddField(
            model_name='whitelabelling',
            name='has_main_header',
            field=models.BooleanField(default=True, verbose_name='Montrer le bandeau générique ?'),
        ),
        migrations.AlterField(
            model_name='whitelabelling',
            name='home_route',
            field=models.CharField(blank=True, default='Home', help_text='La route peut prendre des paramètres sous la forme RouteName:param1=x:param2=y', max_length=100, null=True, verbose_name='Route de la homepage - utilisateur non connectés'),
        ),
        migrations.AlterField(
            model_name='whitelabelling',
            name='home_route_for_administrator',
            field=models.CharField(blank=True, default='Home', help_text='La route peut prendre des paramètres sous la forme RouteName:param1=x:param2=y', max_length=100, null=True, verbose_name='Route de la homepage - administrateurs'),
        ),
        migrations.AlterField(
            model_name='whitelabelling',
            name='home_route_for_advisor',
            field=models.CharField(blank=True, default='Home', help_text='La route peut prendre des paramètres sous la forme RouteName:param1=x:param2=y', max_length=100, null=True, verbose_name='Route de la homepage - conseillers'),
        ),
        migrations.AlterField(
            model_name='whitelabelling',
            name='home_route_for_manager',
            field=models.CharField(blank=True, default='Home', help_text='La route peut prendre des paramètres sous la forme RouteName:param1=x:param2=y', max_length=100, null=True, verbose_name='Route de la homepage - managers'),
        ),
    ]

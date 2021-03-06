# Generated by Django 2.2.9 on 2020-02-12 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('white_labelling', '0013_auto_20200212_0946'),
    ]

    operations = [
        migrations.AlterField(
            model_name='whitelabelling',
            name='home_route',
            field=models.CharField(blank=True, default='AccountLogin', help_text='La route peut prendre des paramètres sous la forme RouteName:param1=x:param2=y', max_length=100, null=True, verbose_name='Route de la homepage - utilisateur non connectés'),
        ),
        migrations.AlterField(
            model_name='whitelabelling',
            name='home_route_for_administrator',
            field=models.CharField(blank=True, default='GroupList', help_text='La route peut prendre des paramètres sous la forme RouteName:param1=x:param2=y', max_length=100, null=True, verbose_name='Route de la homepage - administrateurs'),
        ),
        migrations.AlterField(
            model_name='whitelabelling',
            name='home_route_for_advisor',
            field=models.CharField(blank=True, default='FacContactsList', help_text='La route peut prendre des paramètres sous la forme RouteName:param1=x:param2=y', max_length=100, null=True, verbose_name='Route de la homepage - conseillers'),
        ),
        migrations.AlterField(
            model_name='whitelabelling',
            name='home_route_for_manager',
            field=models.CharField(blank=True, default='GroupList', help_text='La route peut prendre des paramètres sous la forme RouteName:param1=x:param2=y', max_length=100, null=True, verbose_name='Route de la homepage - managers'),
        ),
    ]

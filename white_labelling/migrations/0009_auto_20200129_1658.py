# Generated by Django 2.2.9 on 2020-01-29 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("white_labelling", "0008_auto_20191128_1616"),
    ]

    operations = [
        migrations.AddField(
            model_name="whitelabelling",
            name="matomo_site_id",
            field=models.IntegerField(default=34, verbose_name="SiteId matomo"),
        ),
        migrations.AddField(
            model_name="whitelabelling",
            name="matomo_tracker_file_name",
            field=models.CharField(
                default="piwik", max_length=200, verbose_name="Tracker filename matomo"
            ),
        ),
        migrations.AddField(
            model_name="whitelabelling",
            name="matomo_url",
            field=models.CharField(
                default="https://statspiwik.hespul.org",
                max_length=200,
                verbose_name="Url matomo",
            ),
        ),
    ]
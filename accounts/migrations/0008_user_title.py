# Generated by Django 2.1.4 on 2018-12-10 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("accounts", "0007_user_profile_pic")]

    operations = [
        migrations.AddField(
            model_name="user",
            name="title",
            field=models.CharField(
                blank=True, max_length=100, null=True, verbose_name="Titre ou fonction"
            ),
        )
    ]

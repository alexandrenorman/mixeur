# Generated by Django 2.1.4 on 2019-01-09 16:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [("accounts", "0008_user_title")]

    operations = [
        migrations.AddField(
            model_name="group",
            name="admin_group",
            field=models.ForeignKey(
                blank=True,
                help_text="Groupe parent qui gère l'administration",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="managed_groups",
                to="accounts.Group",
                verbose_name="Groupe administrateur",
            ),
        ),
        migrations.AddField(
            model_name="group",
            name="is_admin",
            field=models.BooleanField(
                default=False,
                help_text="Groupe utilisé pour gérer les groupes par région ?",
                verbose_name="Groupe régional d'administration",
            ),
        ),
    ]
# Generated by Django 2.2.7 on 2019-11-28 09:25

from django.db import migrations
import os


def forwards_func(apps, schema_editor):
    WhiteLabelling = apps.get_model("white_labelling", "WhiteLabelling")
    db_alias = schema_editor.connection.alias

    for wl in WhiteLabelling.objects.using(db_alias).all():

        if not os.path.exists(f"/app/wl-cdn/{wl.domain}"):
            os.mkdir(f"/app/wl-cdn/{wl.domain}")

        for filename, attribute in [
                ("style.css", "css"),
                ("header.html", "header"),
                ("footer.html", "footer"),
        ]:
            value = getattr(wl, attribute)

            if value is not None:
                f = open(os.path.join(f"/app/wl-cdn/{wl.domain}", filename), "w")
                f.write(value)
                f.close()
            

def reverse_func(apps, schema_editor):
    WhiteLabelling = apps.get_model("white_labelling", "WhiteLabelling")
    db_alias = schema_editor.connection.alias

    for wl in WhiteLabelling.objects.using(db_alias).all():
        for filename, attribute in [
                ("style.css", "css"),
                ("header.html", "header"),
                ("footer.html", "footer"),
        ]:

            try:
                f = open(os.path.join(f"/app/wl-cdn/{wl.domain}", filename), "r")
            except Exception:
                pass
            else:
                value = f.read()
                f.close()
                setattr(wl, attribute, value)
                
        wl.save()


class Migration(migrations.Migration):

    dependencies = [
        ('white_labelling', '0006_whitelabelling_clientselfcreation_is_active'),
    ]

    operations = [
        migrations.RunPython(forwards_func, reverse_func),
        migrations.RemoveField(
            model_name='whitelabelling',
            name='css',
        ),
        migrations.RemoveField(
            model_name='whitelabelling',
            name='favicon',
        ),
        migrations.RemoveField(
            model_name='whitelabelling',
            name='footer',
        ),
        migrations.RemoveField(
            model_name='whitelabelling',
            name='header',
        ),
    ]

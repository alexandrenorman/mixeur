# Generated by Django 2.1.5 on 2019-03-10 15:33

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('autodiag_copro', '0002_auto_20190226_1610'),
    ]

    operations = [
        migrations.AlterField(
            model_name='diagnostic',
            name='comments',
            field=ckeditor.fields.RichTextField(blank=True, null=True, verbose_name='Commentaires'),
        ),
    ]

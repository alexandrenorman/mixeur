from django.contrib.postgres.operations import TrigramExtension
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fac', '0015_memberoforganization_owning_group'),
    ]

    operations = [
        # Note: needs superadmin privileges on database, otherwise launch this
        # manually on the DB: `CREATE EXTENSION IF NOT EXISTS pg_trgm;`
        TrigramExtension(),
    ]

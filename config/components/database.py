# -*- coding: utf-8 -*-
import environ

env = environ.Env()

# ## Database ##################################

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

MIGRATION_MODULES = {}
DATABASES = {}
DATABASES["default"] = env.db("DATABASE_URL")

# ## /Database ##################################

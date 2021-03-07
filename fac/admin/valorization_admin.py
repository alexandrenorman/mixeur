# -*- coding: utf-8 -*-
from django.contrib import admin

from ..models import Valorization


@admin.register(Valorization)
class ValorizationAdmin(admin.ModelAdmin):
    base_model = Valorization
    exclude = []

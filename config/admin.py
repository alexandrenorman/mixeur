from django.contrib import admin
from django.contrib.admin import AdminSite

from fac.admin.admin_views import import_csv


class MyAdminSite(AdminSite):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._registry.update(admin.site._registry)

        for model, model_admin in self._registry.items():
            model_admin.admin_site = self

    def get_urls(self):
        from django.urls import path

        urls = super().get_urls()
        urls += [path("fac/import_csv/", self.admin_view(import_csv))]
        return urls


admin_site = MyAdminSite()

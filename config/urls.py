# -*- coding: utf-8 -*-

from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.urls import re_path
from django.views.generic.base import RedirectView

from rest_framework_jwt.views import refresh_jwt_token

from accounts.views import CustomObtainJSONWebToken

from ckeditor_custom.views import CkEditorUpload

from config.admin import admin_site

from core.views import AppInfosView

urlpatterns = [
    # JWT auth
    url(r"^api/v1/auth/login", include("rest_framework.urls")),
    url(r"^api/v1/auth/obtain_token/", CustomObtainJSONWebToken.as_view()),
    url(r"^api/v1/auth/refresh_token/", refresh_jwt_token),
    # API
    url(r"^api/v1/app_infos", AppInfosView.as_view(), name="app_infos"),
    url(r"^api/v1/accounts/", include("accounts.urls", namespace="profile")),
    url(r"^api/v1/cti/", include("cti.urls", namespace="cti")),
    url(
        r"^api/v1/white_labelling/",
        include("white_labelling.urls", namespace="white_labelling"),
    ),
    url(r"^api/v1/territories/", include("territories.urls", namespace="territories")),
    url(r"^api/v1/ckeditor/upload/", CkEditorUpload.as_view(), name="ckeditor_upload"),
    url(
        r"^api/v1/visit-report/", include("visit_report.urls", namespace="visit_report")
    ),
    url(r"^api/v1/actimmo-map/", include("actimmo_map.urls", namespace="actimmo_map")),
    url(
        r"^api/v1/autodiag_copro/",
        include("autodiag_copro.urls", namespace="autodiag_copro"),
    ),
    url(
        r"^api/v1/custom-forms/", include("custom_forms.urls", namespace="custom_forms")
    ),
    url(r"^api/v1/dialogwatt/", include("dialogwatt.urls", namespace="dialogwatt")),
    url(
        r"^api/v1/pdf_generator/",
        include("pdf_generator.urls", namespace="pdf_generator"),
    ),
    url(r"^api/v1/energies/", include("energies.urls", namespace="energies")),
    url(r"^api/v1/thermix/", include("thermix.urls", namespace="thermix")),
    url(r"^api/v1/ecorenover/", include("ecorenover.urls", namespace="ecorenover")),
    url(r"^api/v1/fac/", include("fac.urls", namespace="fac")),
    # some adblockers are triggered by /v1/newsletters
    url(r"^api/v1/infolettres/", include("newsletters.urls", namespace="newsletters")),
    url(r"^api/v1/experiences/", include("experiences.urls", namespace="experiences")),
    url(r"^api/v1/messaging/", include("messaging.urls", namespace="messaging")),
    url(r"^api/v1/listepro/", include("listepro.urls", namespace="listepro")),
    # django
    url(r"^admin/", admin_site.urls),
    url(r"^_nested_admin/", include("nested_admin.urls")),
    url(r"^$", RedirectView.as_view(url="/admin/", permanent=False), name="index"),
]


try:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
except:  # NOQA
    pass


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

    urlpatterns = [
        url(r"^docs/", include("django.contrib.admindocs.urls"))
    ] + urlpatterns

    if "silk" in settings.INSTALLED_APPS:
        urlpatterns += [re_path(r"^silk/", include("silk.urls", namespace="silk"))]

    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [
            url(r"^__debug__/", include(debug_toolbar.urls, namespace="debug_toolbar"))
        ] + urlpatterns

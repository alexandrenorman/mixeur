# -*- coding: utf-8 -*-
import socket
import time

from django.db.utils import ProgrammingError
from django.template import loader

import environ

import sentry_sdk

from config import settings

from helpers.strings import print_boxed


def _get_tls_conf(TRAEFIK_TLS_CONF):
    traefik_tls_conf = "{}"
    if TRAEFIK_TLS_CONF == "letsencrypt":
        traefik_tls_conf = """
        certResolver: letsencrypt-http
        """
    # For dev we just need to keep empty to have "tls: {}""
    # (so traefik will use default certificate as defined in certificates.yml)
    return traefik_tls_conf


def _get_container_name(short_name, attempt=1):
    """
    Return the FQDN of the container short-named `short_name`
    _get_container_name('nginx') => "mixeur_nginx_1'
    """
    MAX_ATTEMPTS = 5
    try:
        hostnames = socket.gethostbyaddr(short_name)
        container_name = hostnames[0].split(".")[0]
        print(f"* Found {short_name} server : {container_name}")
        return container_name
    except socket.gaierror:
        print(f"* NO SERVER FOUND FOR {short_name}")
        if attempt <= MAX_ATTEMPTS:
            print(f"  Retrying in 1 second... ({attempt}/{MAX_ATTEMPTS})")
            time.sleep(1)
            _get_container_name(short_name, attempt + 1)
        return None


def _write_traefik_configuration(content):
    try:
        old_file = open("/app/traefik-conf/configuration.yaml", "r").read()
    except FileNotFoundError:
        old_file = ""

    if old_file != content:
        f = open("/app/traefik-conf/configuration.yaml", "w")
        f.write(content)
        f.close()
        print(" => Traefik file has been changed")
    else:
        print(" => NO CHANGE IN FILE, traefik file not changed")

    return


def generate_traefik_configuration():  # NOQA: C901, CFQ001
    env = environ.Env()
    TRAEFIK_AUTOCONFIG = env.bool("TRAEFIK_AUTOCONFIG", default=False)
    TRAEFIK_REDIRECT_HTTPS = env.str("TRAEFIK_REDIRECT_HTTPS", default=True)
    TRAEFIK_TLS_CONF = env.str("TRAEFIK_TLS_CONF", default="letsencrypt")
    TRAEFIK_USE_AUTH = env.str("TRAEFIK_USE_AUTH", default=True)
    BACKEND = env.str("TRAEFIK_BACKEND", default=None)
    MAIL_NAME = env.str("TRAEFIK_MAIL", default=None)
    NGINX_NAME = env.str("TRAEFIK_NGINX", default="nginx")
    WHITE_LABELLING_FORCE = env.str("WHITE_LABELLING_FORCE", default=None)

    from white_labelling.models import WhiteLabelling

    if WHITE_LABELLING_FORCE:
        print_boxed(f"All WhiteLabellings are replaced by : {WHITE_LABELLING_FORCE}")
        # Inactive other domains and create forced one
        WhiteLabelling.objects.exclude(domain=WHITE_LABELLING_FORCE).update(
            is_active=False
        )
        wl, created = WhiteLabelling.objects.get_or_create(
            domain=WHITE_LABELLING_FORCE,
            defaults={
                "site_title": "mixeur",
                "is_neutral_for_newsletters": False,
                "dialogwatt_is_active": True,
                "enable_django_admin": True,
                "fac_hide_lists": False,
                "fac_statistics_is_active": True,
                "newsletters_is_active": True,
                "experiences_is_active": True,
                "ecorenover_is_active": True,
                "ecorenover_iframe_is_active": False,
                "old_thermix_is_active": False,
                "thermix_is_active": True,
                "home_route_for_client": "DashboardClient",
            },
        )

    if not TRAEFIK_AUTOCONFIG:
        print_boxed("NO WhiteLabelling Generation")
        return

    print_boxed("Starting WhiteLabelling Generation")

    if settings.DEBUG:
        wl, created = WhiteLabelling.objects.get_or_create(
            domain="mixeur.docker.local",
            defaults={
                "site_title": "mixeur",
                "is_neutral_for_newsletters": False,
                "dialogwatt_is_active": True,
                "enable_django_admin": True,
                "fac_hide_lists": False,
                "fac_statistics_is_active": True,
                "newsletters_is_active": True,
                "experiences_is_active": True,
                "ecorenover_is_active": True,
                "ecorenover_iframe_is_active": False,
                "old_thermix_is_active": False,
                "thermix_is_active": True,
                "home_route_for_client": "DashboardClient",
            },
        )
        if created:
            print("* DEBUG mode, auto creating mixeur.docker.local")

        wl, created = WhiteLabelling.objects.get_or_create(
            domain="newsletters.docker.local",
            defaults={
                "site_title": "mixeur",
                "is_neutral_for_newsletters": True,
                "dialogwatt_is_active": False,
                "enable_django_admin": False,
                "fac_is_active": False,
                "fac_statistics_is_active": False,
                "newsletters_is_active": True,
                "experiences_is_active": False,
                "ecorenover_is_active": False,
                "ecorenover_iframe_is_active": False,
                "old_thermix_is_active": False,
                "thermix_is_active": False,
                "has_breadcrumb": False,
                "has_menu": False,
                "has_main_header": False,
            },
        )
        if created:
            print("* DEBUG mode, auto creating newsletters.docker.local")

    nginx_name = _get_container_name(NGINX_NAME)

    if not nginx_name:
        print_boxed("ERROR: Unable to find nginx long hostname")
        sentry_sdk.capture_exception(RuntimeError("Unable to find nginx long hostname"))
        return

    mail_name = None

    if MAIL_NAME:
        if MAIL_NAME == "True":
            MAIL_NAME = "mail"
        mail_name = _get_container_name(MAIL_NAME)

    if not mail_name:
        print("* no mailhog")

    # Fallback to default backend used for prod (nginx listen to port 81)
    backend = BACKEND if BACKEND else f"{nginx_name}:81"

    print(f"* backend django: {backend}")

    print("* generate traefik configurations:")
    try:
        wl_list = list(
            WhiteLabelling.objects.filter(is_active=True)
            .exclude(domain="nginx")
            .order_by("domain")
        )
    except ProgrammingError:
        print("* Model WhiteLabelling not existing -> DO MIGRATE !!")
        print("* no traefik configuration")
        print("----------------------------------")
        return

    content = loader.render_to_string(
        "white_labelling/traefik.yaml",
        {
            "wl_list": wl_list,
            "nginx_name": nginx_name,
            "mail_name": mail_name,
            "backend": backend,
            "traefik_redirect_https": TRAEFIK_REDIRECT_HTTPS,
            "traefik_tls_conf": _get_tls_conf(TRAEFIK_TLS_CONF),
            "use_auth": TRAEFIK_USE_AUTH,
        },
    )

    if wl_list:
        for wl in wl_list:
            print(f"  - {wl.domain}{' - API access'*wl.enable_django_admin}")
    else:
        print_boxed(
            "ERROR: no WhiteLabelling found !!! You must create at least one using the shell"
        )
        sentry_sdk.capture_exception(
            ValueError(
                "no WhiteLabelling found !!! You must create at least one using the shell"
            )
        )
        return

    _write_traefik_configuration(content)

    print("----------------------------------")

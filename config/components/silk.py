from config.components.applications import INSTALLED_APPS
from config.components.middleware import MIDDLEWARE

INSTALLED_APPS += ("silk",)
MIDDLEWARE += ("silk.middleware.SilkyMiddleware",)
SILKY_PYTHON_PROFILER = True
SILKY_PYTHON_PROFILER_BINARY = SILKY_PYTHON_PROFILER


# Silk is reachable from http://api-mixeur.docker.local/silk/

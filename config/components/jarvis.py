# -*- coding: utf-8 -*-
import logging

import environ


env = environ.Env()
logger = logging.getLogger(__name__)

# ## Jarvis configuration ##################################

JARVIS_EMAIL = env("JARVIS_EMAIL", default="")
JARVIS_PASSWORD = env("JARVIS_PASSWORD", default="")
JARVIS_HOST = env("JARVIS_HOST", default="")
JARVIS_PORT = env("JARVIS_PORT", default="")
JARVIS_DELETE = env.bool("JARVIS_DELETE", default=True)

if JARVIS_EMAIL:
    logger.warning("----------------------------------")
    logger.warning("Starting JARVIS support.")
    logger.warning("----------------------------------")
else:
    logger.warning("----------------------------------")
    logger.warning("No JARVIS support.")
    logger.warning("----------------------------------")

# ## /Jarvis configuration ##################################

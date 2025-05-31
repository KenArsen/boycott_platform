from .base import *

# Отладка
DEBUG = env.bool("DEBUG", default=True)
DOMAIN = env.str("DOMAIN", default="http://localhost:8000")

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default="*")

TIME_ZONE = env.str("TIME_ZONE", default="UTC")

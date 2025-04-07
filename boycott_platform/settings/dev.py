import dj_database_url

from .base import *

# Отладка
DEBUG = env.bool("DEBUG", default=True)

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default="*")

DATABASES = {"default": dj_database_url.parse(env.str("DATABASE_URL"))}

TIME_ZONE = env.str("TIME_ZONE", default="UTC")

import os

from django.core.wsgi import get_wsgi_application

from boycott_platform.settings.environment import env

environment = env.str("DJANGO_ENV", default="dev")

assert environment in ["dev", "prod"], f"Неверное значение DJANGO_ENV: {environment}. Ожидается 'dev' или 'prod'."

print(f"Запуск с окружением: {environment}")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", f"boycott_platform.settings.{environment}")

application = get_wsgi_application()

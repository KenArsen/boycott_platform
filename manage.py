#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

from boycott_platform.settings.environment import env


def main():
    """Run administrative tasks."""
    environment = env.str("DJANGO_ENV", default="dev")

    assert environment in ["dev", "prod"], f"Неверное значение DJANGO_ENV: {environment}. Ожидается 'dev' или 'prod'."

    print(f"Запуск с окружением: {environment}")

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", f"boycott_platform.settings.{environment}")

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()

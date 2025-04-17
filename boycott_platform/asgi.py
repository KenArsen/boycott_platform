import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

from apps.assistant.routing import websocket_urlpatterns
from boycott_platform.settings.environment import env

environment = env.str("DJANGO_ENV", default="dev")

assert environment in ["dev", "prod"], f"Неверное значение DJANGO_ENV: {environment}. Ожидается 'dev' или 'prod'."

print(f"Запуск с окружением: {environment}")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", f"boycott_platform.settings.{environment}")

# application = get_asgi_application()
application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": AuthMiddlewareStack(URLRouter(websocket_urlpatterns)),
    }
)

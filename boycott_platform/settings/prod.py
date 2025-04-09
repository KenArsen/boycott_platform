import dj_database_url

from .base import *

DEBUG = env.bool("DEBUG", default=False)

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["yourdomain.com", "www.yourdomain.com"])

DOMAIN = env.str("DOMAIN", default="https://boycott.com")

DATABASES = {"default": dj_database_url.parse(env.str("DATABASE_URL"))}

TIME_ZONE = env.str("TIME_ZONE", default="UTC")

# Статические файлы (собираются в STATIC_ROOT)
STATIC_ROOT = BASE_DIR / "staticfiles"

# Дополнительные настройки безопасности
SECURE_SSL_REDIRECT = True  # Перенаправление на HTTPS
SESSION_COOKIE_SECURE = True  # Куки только через HTTPS
CSRF_COOKIE_SECURE = True  # CSRF только через HTTPS
SECURE_BROWSER_XSS_FILTER = True  # Защита от XSS
SECURE_CONTENT_TYPE_NOSNIFF = True  # Защита от MIME-типов
X_FRAME_OPTIONS = "DENY"  # Запрет встраивания в iframe

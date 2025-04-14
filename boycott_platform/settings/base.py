from pathlib import Path

from django.conf.locale import LANG_INFO
from django.utils.translation import gettext_lazy as _

from .environment import env

BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = env.str("SECRET_KEY")

INSTALLED_APPS = [
    # first party apps
    "jazzmin",
    "modeltranslation",
    # second party apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # third party apps
    # local apps
    "apps.core.apps.CoreConfig",
    "apps.account.apps.AccountConfig",
    "apps.product.apps.ProductConfig",
    "apps.assistant.apps.AssistantConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "boycott_platform.urls"
AUTH_USER_MODEL = "account.User"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "boycott_platform.wsgi.application"

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

JAZZMIN_SETTINGS = {
    "site_title": "Boycott Admin",
    "site_header": "Boycott",
    "site_brand": "Boycott",
    "site_logo_classes": "img-circle",
    "welcome_sign": "Welcome to the Boycott Admin!",
    "search_model": ["account.User", "product.Product"],
    "user_avatar": None,
    "topmenu_links": [
        {"name": "Home", "url": "admin:index", "permissions": ["auth.view_user"]},
        {"name": "Users", "model": "account.User", "url": "/admin/account/user/"},
        {
            "name": "Products",
            "model": "product.Product",
            "url": "/admin/product/product/",
        },
    ],
    "show_sidebar": True,
    "navigation_expanded": True,
    "hide_apps": [],
    "hide_models": [],
    "order_with_respect_to": ["account"],
    "icons": {
        "account": "fas fa-users-cog",
        "account.User": "fas fa-user",
        "auth.Group": "fas fa-users",
        "account.Invitation": "fas fa-envelope-open-text",
        "sites.Site": "fas fa-globe",
        "product.Product": "fas fa-box",
        "product.Category": "fas fa-tags",
        "product.Reason": "fas fa-exclamation-triangle",
        "product.Review": "fas fa-comment-alt",
    },
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",
    "related_modal_active": False,
    "use_google_fonts_cdn": True,
    "show_ui_builder": False,
    "changeform_format": "horizontal_tabs",
    "changeform_format_overrides": {
        "auth.account": "collapsible",
        "auth.group": "vertical_tabs",
    },
    "language_chooser": False,
}

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = env.str("EMAIL_HOST", default="smtp.gmail.com")
EMAIL_PORT = env.int("EMAIL_PORT", default=587)
EMAIL_HOST_USER = env.str("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = env.str("EMAIL_HOST_PASSWORD")
EMAIL_USE_TLS = env.bool("EMAIL_USE_TLS", default=True)
EMAIL_USE_SSL = env.bool("EMAIL_USE_SSL", default=False)

CELERY_BROKER_URL = env.str("CELERY_BROKER_URL")
CELERY_RESULT_BACKEND = env.str("CELERY_RESULT_BACKEND")
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"

# Internationalization settings
LANGUAGE_CODE = "ru-ru"
LANGUAGES = [
    ("en", _("English")),
    ("ru", _("Russian")),
    ("kg", _("Kyrgyz")),
]

MODELTRANSLATION_LANGUAGES = ("en", "ru", "kg")
MODELTRANSLATION_DEFAULT_LANGUAGE = "en"

LANG_INFO.update(
    {
        "kg": {
            "bidi": False,
            "code": "kg",
            "name": "Kyrgyz",
            "name_local": "Кыргызча",
        },
    }
)

USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]

MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

SITE_ID = env.int("SITE_ID", default=1)

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from apps.core.views.home import home_view

urlpatterns = [
    path("home/", home_view, name="home"),
    path("admin/", admin.site.urls),
    path("accounts/", include("apps.account.urls", namespace="account")),
    path("assistant/", include("apps.assistant.urls", namespace="assistant")),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.urls import path
from .views import get_ask

app_name = "assistant"

urlpatterns = [
    path("ask-me/", get_ask, name="ask-me"),
]

# Добавьте эти строки в urls.py
from django.urls import path

from apps.assistant.views.boycott_asistant import chatbot_ui, search_product_api

app_name = "assistant"

urlpatterns = [
    path("", chatbot_ui, name="chatbot_ui"),
    path("search-product/", search_product_api, name="search_product_api"),
]

# Добавьте эти строки в urls.py
from django.urls import path
from apps.assistant.views import chat, simple

app_name="assistant"

urlpatterns = [
    # Другие URL маршруты
    path('chat/', chat.chat_view, name='chat_view'),
    path('api/chat/', chat.chat_api, name='chat_api'),
    path('simple/', simple.chat_api, name='chat_api'),
]
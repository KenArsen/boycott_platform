from django.urls import path

from apps.assistant.views import chat

app_name = "assistant"

urlpatterns = [
    path("chat/", chat, name="chat"),
]

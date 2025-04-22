from django.urls import re_path

from apps.assistant.services import consumers

websocket_urlpatterns = [
    re_path(r"ws/chat/", consumers.AIChatConsumer.as_asgi()),
]

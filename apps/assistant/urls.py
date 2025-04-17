from django.urls import path

from apps.assistant.views import index, room

app_name = "assistant"

urlpatterns = [
    path("", index, name="index"),
    path("<str:room_name>/", room, name="room"),
]

from django.shortcuts import render


def index(request):
    return render(request, "index.html")


def room(request, room_name):
    return render(request, "ai_chat.html", {"room_name": room_name})

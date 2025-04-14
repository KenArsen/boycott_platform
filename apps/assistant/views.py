from django.http import HttpResponse
from django.shortcuts import render

from apps.assistant.forms import AskForm

from apps.assistant.services.ask import ask_ai_about_product


def get_ask(request):
    if request.method == "POST":
        form = AskForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data["content"]
            ask = ask_ai_about_product(content)
            return HttpResponse(ask)
        else:
            return HttpResponse(form.errors)
    else:
        form = AskForm()
    return render(request, 'ask.html', {'form': form})
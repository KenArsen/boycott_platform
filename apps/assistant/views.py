from django.shortcuts import render

from apps.assistant.forms import AskForm
from apps.assistant.services.ask import ask_product_assistant


def assistant_view(request, product_id):
    if request.method == "POST":
        form = AskForm(request.POST)
        if form.is_valid():
            response = ask_product_assistant(product_id, request.POST.get("message"))
            return render(request, "", {"response": response})
    else:
        form = AskForm()
    return render(request, "", {"form": form})

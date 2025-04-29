import json

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from apps.assistant.services.rag import SimpleProductKnowledgeBase

knowledge_base = SimpleProductKnowledgeBase()


@csrf_exempt
def chat_api(request):
    if request.method == "POST":
        try:
            body = json.loads(request.body)  # <--- читаем JSON из тела запроса
            user_message = body.get("message")
        except json.JSONDecodeError:
            return JsonResponse({"error": "Невалидный JSON"}, status=400)

        if not user_message:
            return JsonResponse({"error": "Пустое сообщение"}, status=400)

        answer, product = knowledge_base.ask(user_message)
        print(answer, product)

        return JsonResponse({"response": answer, "product": product})
    return render(request, "simple.html")

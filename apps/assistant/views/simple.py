from apps.assistant.services.rag import SimpleProductKnowledgeBase
from django.http import JsonResponse

knowledge_base = SimpleProductKnowledgeBase()


def chat_api(request):
    user_message = request.POST.get('message')

    answer = knowledge_base.ask(user_message)

    return JsonResponse({"response": answer})

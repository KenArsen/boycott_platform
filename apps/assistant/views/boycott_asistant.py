import json

import openai
from django.conf import settings
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt

from apps.assistant.services.embedding import QueryEngine
from apps.product.models import Product

# Установите ваш API-ключ OpenAI
openai.api_key = settings.OPENAI_API_KEY


def chatbot_ui(request):
    return render(
        request,
        "boycott_assistant.html",
    )


@csrf_exempt
def search_product_api(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            query = data.get("query", "").strip().lower()

            # Основной поиск по базе данных
            products = (
                Product.objects.select_related("category", "boycott_reason")
                .prefetch_related("alternative_products")
                .filter(
                    Q(name__icontains=query)
                    | Q(name_ru__icontains=query)
                    | Q(name_en__icontains=query)
                    | Q(name_kg__icontains=query)
                )
            )

            if products.exists():
                html = render_to_string("product_card.html", {"products": products})
                return JsonResponse({"success": True, "html": html})

            products = (
                Product.objects.select_related("category", "boycott_reason")
                .prefetch_related("alternative_products")
                .filter(id__in=[str(i["id"]) for i in QueryEngine().generate_response(query).get("results", [])])
            )

            if products.exists():
                html = render_to_string("product_card.html", {"products": products})
                return JsonResponse({"success": True, "html": html})

            return JsonResponse(
                {
                    "success": False,
                    "html": f'К сожалению, я не нашел информации о продукте "{query}". '
                    f"Попробуйте ввести другое название.",
                }
            )

        except Exception as e:
            return JsonResponse({"success": False, "html": f"Ошибка: {str(e)}"})

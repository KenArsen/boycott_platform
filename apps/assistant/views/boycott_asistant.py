import json

from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt

from apps.product.models import Product


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

            product = (
                Product.objects.select_related("category", "boycott_reason")
                .prefetch_related("alternative_products")
                .filter(name__icontains=query)
                .first()
            )

            if not product:
                return JsonResponse(
                    {
                        "success": False,
                        "html": f'К сожалению, я не нашел информации о продукте "{query}". '
                        f"Попробуйте ввести другое название.",
                    }
                )

            html = render_to_string("product_card.html", {"product": product})
            return JsonResponse({"success": True, "html": html})
        except Exception as e:
            return JsonResponse({"success": False, "html": f"Ошибка: {str(e)}"})

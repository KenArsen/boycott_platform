import json

import openai
from django.conf import settings
from django.db import connection
from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt

from apps.product.models import Product

# Установите ваш API-ключ OpenAI
openai.api_key = settings.OPENAI_API_KEY


def chatbot_ui(request):
    return render(
        request,
        "boycott_assistant.html",
    )


# @csrf_exempt
# def search_product_api(request):
#     if request.method == "POST":
#         try:
#             data = json.loads(request.body)
#             query = data.get("query", "").strip().lower()
#
#             product = (
#                 Product.objects.select_related("category", "boycott_reason")
#                 .prefetch_related("alternative_products")
#                 .filter(name__icontains=query)
#                 .first()
#             )
#
#             if not product:
#                 return JsonResponse(
#                     {
#                         "success": False,
#                         "html": f'К сожалению, я не нашел информации о продукте "{query}". '
#                         f"Попробуйте ввести другое название.",
#                     }
#                 )
#
#             html = render_to_string("product_card.html", {"product": product})
#             return JsonResponse({"success": True, "html": html})
#         except Exception as e:
#             return JsonResponse({"success": False, "html": f"Ошибка: {str(e)}"})


@csrf_exempt
def search_product_api(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            query = data.get("query", "").strip()

            # Простой поиск по названию продукта
            product = (
                Product.objects.select_related("category", "boycott_reason")
                .prefetch_related("alternative_products")
                .filter(name__icontains=query)
                .first()
            )

            if product:
                html = render_to_string("product_card.html", {"product": product})
                return JsonResponse({"success": True, "html": html})

            # Генерация SQL-запроса с помощью OpenAI
            prompt = (
                f'На основе следующего запроса пользователя:\n"{query}"\n'
                f"сгенерируй SQL-запрос для выборки соответствующих продуктов из базы данных."
                f"Таблица называется 'product_product', и содержит поля: "
                f"'id', 'name', 'description', 'is_boycotted', 'boycott_reason_id', 'category_id'. "
                f"Таблица 'product_reason' содержит поля: 'id', 'title'. "
                f"Таблица 'product_category' содержит поля: 'id', 'name'. "
                f"Пример запроса: SELECT * FROM product_product WHERE is_boycotted = TRUE;"
            )

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "Ты помощник, который генерирует SQL-запросы на основе пользовательских запросов.",
                    },
                    {"role": "user", "content": prompt},
                ],
                temperature=0.2,
                max_tokens=150,
                n=1,
                stop=None,
            )

            sql_query = response["choices"][0]["message"]["content"].strip()

            # Выполнение сгенерированного SQL-запроса
            with connection.cursor() as cursor:
                cursor.execute(sql_query)
                columns = [col[0] for col in cursor.description]
                rows = cursor.fetchall()
                products = [dict(zip(columns, row)) for row in rows]

            if not products:
                return JsonResponse(
                    {
                        "success": False,
                        "html": f'К сожалению, не удалось найти продукты по запросу "{query}".'
                        f" Попробуйте изменить запрос.",
                    }
                )

            # Рендеринг списка продуктов
            html = render_to_string("product_list.html", {"products": products})
            return JsonResponse({"success": True, "html": html})

        except Exception as e:
            return JsonResponse(
                {
                    "success": False,
                    "error": str(e),
                    "html": "Произошла ошибка при обработке вашего запроса. Пожалуйста, попробуйте снова.",
                }
            )

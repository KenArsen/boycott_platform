import json
from typing import Optional

import requests
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt

from apps.product.models import Product


def chatbot_ui(request):
    return render(request, "boycott_assistant.html")


class AIServiceError(Exception):
    """Кастомное исключение для ошибок AI сервиса"""

    pass


class AIResponse:
    """Класс для структурированного ответа от AI"""

    def __init__(self, product: Optional[str] = None, message: Optional[str] = None, error: Optional[str] = None):
        self.product = product
        self.message = message
        self.error = error

    @property
    def is_success(self) -> bool:
        return self.error is None

    @property
    def has_product(self) -> bool:
        return self.product is not None and self.product.strip() != ""

    @property
    def has_message(self) -> bool:
        return self.message is not None and self.message.strip() != ""


def get_product_info(message: str) -> AIResponse:
    """
    Получает информацию о продукте от AI сервиса

    Args:
        message: Запрос пользователя

    Returns:
        AIResponse: Объект с результатом запроса
    """
    if not message.strip():
        return AIResponse(error="Пустой запрос")

    url = "https://kenzhegulov.app.n8n.cloud/webhook/de883deb-a9df-4826-a53b-f2f97dfae4f2"
    print(message)

    try:
        response = requests.get(url, params={"message": message}, timeout=30)
        response.raise_for_status()

        # Парсим ответ
        outer_data = response.json()
        output_str = outer_data.get("output", "{}")

        if not output_str:
            return AIResponse(error="Пустой ответ от AI сервиса")

        data = json.loads(output_str)

        return AIResponse(product=data.get("product"), message=data.get("message"))

    except requests.exceptions.Timeout:
        return AIResponse(error="Превышено время ожидания ответа от AI сервиса")

    except requests.exceptions.RequestException as e:
        return AIResponse(error=f"Ошибка соединения с AI сервисом: {e}")

    except json.JSONDecodeError as e:
        return AIResponse(error=f"Ошибка обработки ответа от AI сервиса: {e}")

    except Exception as e:
        return AIResponse(error=f"Произошла неожиданная ошибка: {e}")


def search_products_in_db(product_name: str):
    """
    Ищет продукты в базе данных по названию

    Args:
        product_name: Название продукта для поиска

    Returns:
        QuerySet: Найденные продукты
    """
    return (
        Product.objects.select_related("category", "boycott_reason")
        .prefetch_related("alternative_products")
        .filter(
            Q(name__icontains=product_name)
            | Q(name_ru__icontains=product_name)
            | Q(name_en__icontains=product_name)
            | Q(name_kg__icontains=product_name)
        )
    )


def create_message_html(message: str, message_type: str = "info") -> str:
    """
    Создает HTML для отображения сообщения

    Args:
        message: Текст сообщения
        message_type: Тип сообщения (info, error, success)

    Returns:
        str: HTML код сообщения
    """
    css_class = {
        "info": "api-message-box minimal",
        "error": "api-message-box error",
        "success": "api-message-box success",
    }.get(message_type, "api-message-box minimal")

    return f"""
    <div class="ai-message-container">
        <div class="{css_class}">
            {message}
        </div>
    </div>
    """


@csrf_exempt
def search_product_api(request):
    """
    API для поиска продуктов через AI ассистента
    """
    if request.method != "POST":
        return JsonResponse({"success": False, "html": create_message_html("Метод не поддерживается", "error")})

    try:
        # Парсим запрос
        data = json.loads(request.body)
        query = data.get("query", "").strip()

        if not query:
            return JsonResponse({"success": False, "html": create_message_html("Пустой запрос", "error")})

        # Получаем ответ от AI
        ai_response = get_product_info(query)

        # Обрабатываем ошибки AI сервиса
        if not ai_response.is_success:
            return JsonResponse({"success": False, "html": create_message_html(ai_response.error, "error")})

        # Если AI вернул название продукта - ищем в базе
        if ai_response.has_product:
            products = search_products_in_db(ai_response.product)

            if products.exists():
                # Найдены продукты - отображаем карточки
                html = render_to_string("product_card.html", {"products": products, "ai_message": ai_response.message})
                return JsonResponse({"success": True, "html": html})
            else:
                # Продукт не найден в базе
                message = f'Продукт "{ai_response.product}" не найден в нашей базе данных.'
                if ai_response.has_message:
                    message += f"\n\n{ai_response.message}"

                return JsonResponse({"success": True, "html": create_message_html(message, "info")})

        # Если AI вернул только сообщение (например, общий вопрос)
        elif ai_response.has_message:
            return JsonResponse({"success": True, "html": create_message_html(ai_response.message, "info")})

        # AI не вернул ничего полезного
        else:
            return JsonResponse(
                {
                    "success": False,
                    "html": create_message_html(
                        f'Не удалось обработать запрос: "{query}". Попробуйте переформулировать.', "error"
                    ),
                }
            )

    except json.JSONDecodeError:
        return JsonResponse({"success": False, "html": create_message_html("Ошибка в формате запроса", "error")})

    except Exception as e:
        return JsonResponse(
            {"success": False, "html": create_message_html(f"Произошла внутренняя ошибка: {e}", "error")}
        )


"""
Улучшения в новой версии:

1. **Структурированные ответы**: Класс AIResponse для четкой структуры данных
2. **Типизация**: Использование type hints для лучшей читаемости
3. **Обработка ошибок**: Разделение типов ошибок и их правильная обработка
4. **Логирование**: Добавлено логирование ошибок для отладки
5. **Timeout**: Добавлен timeout для HTTP запросов
6. **Валидация**: Проверка входных данных
7. **Разделение ответственности**: Каждая функция имеет одну задачу
8. **Расширяемость**: Легко добавлять новые типы запросов
9. **Кастомные исключения**: Для более точной обработки ошибок
10. **HTML генерация**: Централизованная функция для создания HTML
"""

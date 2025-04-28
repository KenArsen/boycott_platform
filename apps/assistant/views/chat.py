from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
import json
import logging
import traceback
from apps.assistant.services.rag import ProductKnowledgeBase

# Настраиваем логирование
logger = logging.getLogger(__name__)

# Инициализируем базу знаний при запуске
knowledge_base = None


def initialize_knowledge_base():
    global knowledge_base
    if knowledge_base is None:
        try:
            logger.info("Initializing knowledge base...")
            knowledge_base = ProductKnowledgeBase()
            knowledge_base.build_knowledge_base()
            logger.info("Knowledge base initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing knowledge base: {e}")
            logger.error(traceback.format_exc())


# Отображение страницы чата
def chat_view(request):
    """
    Отображает страницу чата
    """
    return render(request, 'simple.html')


@csrf_exempt
def chat_api(request):
    """
    API для взаимодействия с чат-ботом
    """
    print(request.method)
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get('message', '')

            # Проверяем, инициализирована ли база знаний
            global knowledge_base
            if knowledge_base is None:
                initialize_knowledge_base()
                if knowledge_base is None:
                    return JsonResponse({
                        'error': 'Knowledge base initialization failed. Check logs for details.'
                    }, status=500)

            # Получаем ответ от базы знаний
            answer = knowledge_base.ask(user_message)

            # Ищем продукт, о котором спрашивает пользователь
            from apps.product.models import Product

            # Используем более эффективный запрос
            products = Product.objects.filter(
                name__icontains=user_message
            ).select_related(
                'category', 'boycott_reason'
            ).prefetch_related(
                'alternative_products'
            )[:5]  # Ограничиваем максимальное количество результатов

            mentioned_product = None

            # Находим продукт, который лучше всего соответствует запросу
            for product in products:
                if product.name.lower() in user_message.lower():
                    mentioned_product = product
                    break

            response_data = {
                'text': answer,
                'product': None
            }

            # Если найден продукт, добавляем информацию о нем
            if mentioned_product:
                response_data['product'] = {
                    'id': mentioned_product.id,
                    'name': mentioned_product.name,
                    'is_boycotted': mentioned_product.is_boycotted,
                    'image_url': mentioned_product.image.url if mentioned_product.image else None
                }

                # Если продукт бойкотируется, добавляем информацию о причине
                if mentioned_product.is_boycotted and mentioned_product.boycott_reason:
                    response_data['product']['boycott_reason'] = {
                        'title': mentioned_product.boycott_reason.title,
                        'description': mentioned_product.boycott_reason.description
                    }

                # Добавляем альтернативы более эффективно
                alternatives = []
                for alt in mentioned_product.alternative_products.all()[:5]:  # Ограничиваем количество альтернатив
                    alternatives.append({
                        'id': alt.id,
                        'name': alt.name,
                        'is_kyrgyz_product': alt.is_kyrgyz_product,
                        'image_url': alt.image.url if alt.image else None
                    })

                if alternatives:
                    response_data['product']['alternatives'] = alternatives

            return JsonResponse(response_data)

        except Exception as e:
            logger.error(f"Error in chat_api: {e}")
            logger.error(traceback.format_exc())
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Only POST requests allowed'}, status=405)

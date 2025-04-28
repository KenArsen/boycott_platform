import re
from apps.product.models import Product, Category, Reason


def analyze_user_message(message):
    """
    Анализирует сообщение пользователя и формирует ответ
    """
    # Поиск по названию продукта
    product_match = find_product_in_message(message)
    if product_match:
        return get_product_info(product_match)

    # Поиск по категории
    category_match = find_category_in_message(message)
    if category_match:
        return get_category_info(category_match)

    # Общий запрос о бойкотах
    if 'бойкот' in message or 'причин' in message:
        return get_boycott_info()

    # Если не удалось определить запрос
    return {
        'type': 'text',
        'content': 'Извините, я не понял ваш вопрос. Вы можете спросить о конкретном продукте, категории или причинах бойкота.'
    }


def find_product_in_message(message):
    """
    Находит упоминание продукта в сообщении пользователя
    """
    # Получаем все продукты из базы
    products = Product.objects.all()

    # Ищем упоминания продуктов в сообщении
    for product in products:
        # Используем регулярное выражение для поиска названия продукта
        # с учетом возможных вариаций написания
        if re.search(r'\b' + re.escape(product.name.lower()) + r'\b', message):
            return product

    return None


def find_category_in_message(message):
    """
    Находит упоминание категории в сообщении пользователя
    """
    categories = Category.objects.all()

    for category in categories:
        if re.search(r'\b' + re.escape(category.name.lower()) + r'\b', message):
            return category

    return None


def get_product_info(product):
    """
    Формирует ответ с информацией о продукте
    """
    # Увеличиваем счетчик запросов продукта
    product.query_count += 1
    product.save()

    response = {
        'type': 'product',
        'content': {
            'name': product.name,
            'description': product.description,
            'category': product.category.name,
            'is_boycotted': product.is_boycotted,
            'rating': product.get_rating(),
            'is_kyrgyz_product': product.is_kyrgyz_product,
            'image_url': product.image.url if product.image else None,
        }
    }

    # Если продукт бойкотируется, добавляем информацию о причине
    if product.is_boycotted and product.boycott_reason:
        response['content']['boycott_reason'] = {
            'title': product.boycott_reason.title,
            'description': product.boycott_reason.description
        }

        # Добавляем альтернативы
        alternatives = []
        for alt in product.alternative_products.all():
            alternatives.append({
                'id': alt.id,
                'name': alt.name,
                'rating': alt.get_rating(),
                'is_kyrgyz_product': alt.is_kyrgyz_product,
                'image_url': alt.image.url if alt.image else None,
            })
        response['content']['alternatives'] = alternatives

    # Формируем текстовый ответ
    text_response = format_product_response(product)
    response['text_response'] = text_response

    return response


def format_product_response(product):
    """
    Форматирует текстовый ответ о продукте
    """
    if product.is_boycotted:
        response = f"{product.name} является бойкотируемым продуктом. "

        if product.boycott_reason:
            response += f"Причина: {product.boycott_reason.title}. {product.boycott_reason.description} "

        alternatives = product.alternative_products.all()
        if alternatives:
            response += "Рекомендуемые альтернативы: "
            alt_names = [alt.name for alt in alternatives]
            response += ", ".join(alt_names) + "."

        return response
    else:
        return f"{product.name} не входит в список бойкотируемых продуктов."


def get_category_info(category):
    """
    Формирует ответ с информацией о категории
    """
    # Получаем бойкотируемые продукты в этой категории
    boycotted_products = Product.objects.filter(category=category, is_boycotted=True)

    response = {
        'type': 'category',
        'content': {
            'name': category.name,
            'description': category.description,
            'boycotted_products': []
        }
    }

    # Добавляем информацию о бойкотируемых продуктах
    for product in boycotted_products:
        product_info = {
            'id': product.id,
            'name': product.name,
            'boycott_reason': product.boycott_reason.title if product.boycott_reason else None,
            'image_url': product.image.url if product.image else None,
        }
        response['content']['boycotted_products'].append(product_info)

    # Формируем текстовый ответ
    text_response = f"В категории {category.name} найдено {boycotted_products.count()} бойкотируемых продуктов."
    response['text_response'] = text_response

    return response


def get_boycott_info():
    """
    Возвращает общую информацию о причинах бойкота
    """
    reasons = Reason.objects.all()

    response = {
        'type': 'boycott_info',
        'content': {
            'reasons': []
        }
    }

    for reason in reasons:
        reason_info = {
            'title': reason.title,
            'description': reason.description
        }
        response['content']['reasons'].append(reason_info)

    # Формируем текстовый ответ
    text_response = "Основные причины бойкота продуктов:\n"
    for reason in reasons:
        text_response += f"- {reason.title}: {reason.description}\n"

    response['text_response'] = text_response

    return response
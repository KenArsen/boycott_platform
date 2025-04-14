import requests
from apps.product.models import Product


def ask_ai_about_product(question: str) -> str:
    products = Product.objects.filter(is_boycotted=True).select_related('boycott_reason')[:5]

    context = "Вот некоторые бойкотированные товары:\n"
    for product in products:
        print(product.name)
        context += f"- {product.name}: {product.description}\n"

    # 2. Формируем промпт
    prompt = f"""
    Вот информация о бойкотируемых товарах:
    {context}

    Вопрос пользователя: {question}
    Ответь на русском языке, как специалист.
    """

    try:
        # 3. Отправляем запрос в локальный Ollama-сервер
        response = requests.post(
            "http://host.docker.internal:11434/api/generate",
            json={
                "model": "nous-hermes2",
                "prompt": prompt,
                "stream": False,
            }
        )
    except requests.exceptions.RequestException as e:
        print(e)
    return response.json()["response"]
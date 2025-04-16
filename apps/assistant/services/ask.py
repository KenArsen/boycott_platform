import requests

from apps.product.models import Product


def ask_product_assistant(product_id, user_question):
    product = Product.objects.get(pk=product_id)
    prompt = f"""
Ты — ассистент. Используй только эту информацию о продукте:

Название: EN({product.name_en}), RU({product.name_ru}, KG({product.name_kg})
Описание:  EN({product.description_en})\n\nRU({product.description}\n\nKG({product.description_kg})

Теперь ответь на вопрос пользователя на русском:
"{user_question}"
    """

    try:
        response = requests.post(
            "http://localhost:11434/api/generate", json={"model": "nous-hermes2", "prompt": prompt, "stream": False}
        )
        answer = response.json()["response"].strip().lower()

        return answer
    except requests.exceptions.RequestException as e:
        return f"❌ Ошибка обработки {product.name}: {e}"
    except Exception as e:
        return f"❌ Ошибка обработки {product.name}: {e}"

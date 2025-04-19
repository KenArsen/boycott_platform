import requests
from requests.exceptions import ConnectionError, Timeout


def get_ai_response(message):
    try:
        response = requests.post(
            url="http://host.docker.internal:11434/api/generate",
            json={
                "model": "nous-hermes2",
                "prompt": message,
                "stream": False,
            },
        )
        answer = response.json()["response"].strip().lower()

        return answer
    except ConnectionError:
        return "❌ Не удалось подключиться к API. Возможно, сервер не запущен."
    except Timeout:
        return "⏱️ Время ожидания истекло."
    except Exception as e:
        return f"❌ Ошибка обработки: {e}"

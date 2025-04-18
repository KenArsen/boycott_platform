import requests


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
    except Exception as e:
        return f"❌ Ошибка обработки: {e}"

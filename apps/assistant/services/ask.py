import httpx


async def get_ai_response(message):
    async with httpx.AsyncClient(trust_env=True, timeout=10.0) as client:
        try:
            response = await client.post(
                url="http://host.docker.internal:11434/api/generate",
                json={
                    "model": "nous-hermes2",
                    "prompt": message,
                    "stream": False,
                },
            )
            return response.json()["response"].strip().lower()
        except httpx.RequestError as e:
            return f"❌ Ошибка запроса: {str(e)}"
        except Exception as e:
            return f"❌ Ошибка: {e}"

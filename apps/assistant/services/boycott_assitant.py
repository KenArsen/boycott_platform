# import json
# import re
# import subprocess
# import time
#
# from django.conf import settings
# from openai import OpenAI
#
# 🔑 API-ключ
# client = OpenAI(api_key=settings.OPENAI_API_KEY)
#
# # 📁 Загрузка файла
# file = client.files.create(
#     file=open("simplified_data.json", "rb"),
#     purpose="assistants"
# )
#
# # 🧠 Создание ассистента
# assistant = client.beta.assistants.create(
#     name="Помощник по бойкоту товаров",
#     instructions="""
# Ты — помощник, который использует JSON-файл со списком товаров.
# Каждый товар содержит поля: name, description_ru, is_boycotted, is_kyrgyz_product.
# Ты должен с помощью Python-кода (через code_interpreter) найти товар по названию и вывести краткое описание,
# статус бойкота и т.д.
# """,
#     model="gpt-3.5-turbo-1106",
#     tools=[{"type": "code_interpreter"}],
#     tool_resources={
#         "code_interpreter": {
#             "file_ids": [file.id]
#         }
#     }
# )
#
# # 💬 Поток
# thread = client.beta.threads.create()
#
#
# # 🚀 Функция общения
# def ask_assistant(user_input):
#     # Очистка от невалидных символов
#     user_input = user_input.encode("utf-8", "ignore").decode("utf-8")
#
#     # 1. Отправка сообщения
#     client.beta.threads.messages.create(
#         thread_id=thread.id,
#         role="user",
#         content=user_input
#     )
#
#     # 2. Запуск обработки
#     run = client.beta.threads.runs.create(
#         thread_id=thread.id,
#         assistant_id=assistant.id
#     )
#
#     # 3. Ожидание завершения
#     while True:
#         run_status = client.beta.threads.runs.retrieve(
#             thread_id=thread.id,
#             run_id=run.id
#         )
#         if run_status.status == "completed":
#             break
#         elif run_status.status in ["failed", "cancelled", "expired"]:
#             print("‼️ Ошибка:", run_status.last_error.message if run_status.last_error else "Неизвестная ошибка")
#             return
#         time.sleep(1)
#
#     # 4. Получение ответа
#     messages = client.beta.threads.messages.list(thread_id=thread.id)
#     for message in reversed(messages.data):
#         if message.role == "assistant":
#             print("🧠 Ассистент:", message.content[0].text.value)
#             return
#
#
# # 🔁 Цикл общения
# while True:
#     try:
#         user_input = input("Спроси что угодно: ")
#         ask_assistant(user_input)
#     except KeyboardInterrupt:
#         print("\nЗавершено пользователем.")
#         break

import json
import re
import subprocess


# 🔧 Удаление невалидных символов (surrogate pairs)
def clean_surrogates(text):
    return re.sub(r"[\ud800-\udfff]", "", text)


# 🔄 Очистка всей структуры JSON
def recursive_clean(obj):
    if isinstance(obj, dict):
        return {k: recursive_clean(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [recursive_clean(i) for i in obj]
    elif isinstance(obj, str):
        return clean_surrogates(obj)
    return obj


# 📁 Загрузка и очистка JSON
with open("simplified_data.json", encoding="utf-8", errors="ignore") as f:
    raw_data = json.load(f)
    products = recursive_clean(raw_data)


# 🧠 Генерация промпта
def generate_prompt(query):
    prompt = f"""
У тебя есть база товаров в формате JSON.
Вот пример товаров:

{json.dumps(products, ensure_ascii=False, indent=2)}

Пользователь спрашивает: "{query}"

Найди товар по названию и объясни:
- Что это такое
- Бойкотируется ли
- Кыргызский ли это продукт
Если не найден — скажи, что товар не найден.
"""
    return clean_surrogates(prompt)


# 🚀 Запрос к Ollama
def query_ollama(prompt):
    result = subprocess.run(
        ["ollama", "run", "nous-hermes2"],  # можешь заменить на 'mistral', 'llama3' и т.д.
        input=prompt.encode("utf-8"),
        stdout=subprocess.PIPE,
    )
    return result.stdout.decode("utf-8", errors="ignore")


# 🔁 Общение
while True:
    try:
        question = input("Спроси что угодно: ")
        prompt = generate_prompt(question)
        response = query_ollama(prompt)
        print("\n🧠 Ответ:\n", response)
    except KeyboardInterrupt:
        print("\nЗавершено пользователем.")
        break

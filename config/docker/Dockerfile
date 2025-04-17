# Этап 1: Сборка зависимостей с Poetry
FROM python:3.11-slim AS builder

# Устанавливаем переменные окружения
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Устанавливаем рабочую директорию
WORKDIR /app

# Устанавливаем Poetry
RUN pip install poetry

# Копируем только файлы Poetry для установки зависимостей
COPY pyproject.toml poetry.lock ./

# Устанавливаем зависимости без dev
RUN poetry config virtualenvs.create false \
    && poetry install --without dev --no-interaction --no-ansi --no-root

# Копируем весь проект
COPY . /app

# Этап 2: Runtime-образ
FROM python:3.11-slim

# Устанавливаем переменные окружения
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Устанавливаем рабочую директорию
WORKDIR /app

# Устанавливаем минимальные системные зависимости (для Celery, PostgreSQL и т.д.)
RUN apt-get update && apt-get install -y \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Копируем зависимости и проект из builder
COPY --from=builder /usr/local/lib/python3.11/site-packages/ /usr/local/lib/python3.11/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/
COPY --from=builder /app /app

# Открываем порт для Django
EXPOSE 8000

# Указываем команду по умолчанию (будет переопределена в docker-compose)
#CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
CMD ["sh", "-c", "python manage.py migrate && daphne -b 0.0.0.0 -p 8000 boycott_platform.asgi:application"]
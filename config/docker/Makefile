# Путь к Docker Compose с указанием конфигурационного файла и .env-файла
DOCKER_COMPOSE = docker-compose -f config/docker/docker-compose.yaml --env-file $(shell pwd)/.env

# Сборка Docker-образов
.PHONY: build
build:
	$(DOCKER_COMPOSE) build

# Запуск контейнеров в фоне (рекомендуемый способ для продакшна)
.PHONY: up
up:
	$(DOCKER_COMPOSE) up -d

# Запуск контейнеров в активном терминале (удобно для отладки)
.PHONY: start
start:
	$(DOCKER_COMPOSE) up

# Остановка всех запущенных контейнеров
.PHONY: stop
stop:
	$(DOCKER_COMPOSE) stop

# Остановка и удаление контейнеров
.PHONY: down
down:
	$(DOCKER_COMPOSE) down

# Перезапуск контейнеров
.PHONY: restart
restart:
	$(DOCKER_COMPOSE) restart

# Просмотр логов всех контейнеров (режим "follow")
.PHONY: logs
logs:
	$(DOCKER_COMPOSE) logs -f

# Полная очистка: удаляет контейнеры, образы, тома, висячие зависимости
.PHONY: clean
clean:
	$(DOCKER_COMPOSE) down -v --rmi all --remove-orphans

# Вход в контейнер (оболочка Bash), предполагается, что сервис называется 'web'
.PHONY: shell
shell:
	$(DOCKER_COMPOSE) exec web /bin/bash

# Применение миграций Django (аналог `python manage.py migrate`)
.PHONY: migrate
migrate:
	$(DOCKER_COMPOSE) exec web python manage.py migrate

# Создание суперпользователя (предполагается, что команда определена как `create_admin`)
.PHONY: create-superuser
create-superuser:
	$(DOCKER_COMPOSE) exec web python manage.py create_admin

# Сбор статики Django (например, для деплоя)
.PHONY: collectstatic
collectstatic:
	$(DOCKER_COMPOSE) exec web python manage.py collectstatic --no-input

# Экспорт данных из базы в JSON-файл (фикстуры)
# Параметры:
#   APP — имя приложения или модели (например: products.Product)
#   FILE — имя выходного файла (например: products)
#   DIR — путь к каталогу, где хранить фикстуры (например: apps)
# Пример: make dump APP=products.Product FILE=products DIR=apps
.PHONY: dump
dump:
	$(DOCKER_COMPOSE) exec web python manage.py dumpdata $(APP) --indent 4 --format json > $(DIR)/fixtures/$(FILE).json

# Импорт фикстур обратно в базу данных
# Параметры:
#   FILE — имя JSON-файла (например: products)
#   DIR — каталог, где хранится файл (например: apps)
# Пример: make load FILE=products DIR=apps
.PHONY: load
load:
	$(DOCKER_COMPOSE) exec web python manage.py loaddata $(DIR)/fixtures/$(FILE).json

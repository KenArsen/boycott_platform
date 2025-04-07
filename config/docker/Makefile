# config/docker/Makefile

# Путь к Docker Compose
DOCKER_COMPOSE = docker-compose -f config/docker/docker-compose.yaml
PROJECT_NAME = boycott_platform

# Цель по умолчанию
.PHONY: help
help:
	@echo "Makefile for $(PROJECT_NAME)"
	@echo "Available commands:"
	@echo "  make build    - Build Docker images"
	@echo "  make up       - Start containers in background"
	@echo "  make start    - Start containers in foreground"
	@echo "  make stop     - Stop running containers"
	@echo "  make down     - Stop and remove containers"
	@echo "  make restart  - Restart containers"
	@echo "  make logs     - View container logs"
	@echo "  make clean    - Remove all containers, images, and volumes"
	@echo "  make shell    - Access container shell"

# Сборка Docker-образов
.PHONY: build
build:
	$(DOCKER_COMPOSE) build

# Запуск контейнеров в фоне
.PHONY: up
up:
	$(DOCKER_COMPOSE) up -d

# Запуск контейнеров в фоновом режиме
.PHONY: start
start:
	$(DOCKER_COMPOSE) up

# Остановка контейнеров
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

# Просмотр логов
.PHONY: logs
logs:
	$(DOCKER_COMPOSE) logs -f

# Очистка (удаление контейнеров, образов, томов)
.PHONY: clean
clean:
	$(DOCKER_COMPOSE) down -v --rmi all --remove-orphans

# Доступ к оболочке контейнера (предполагается, что сервис называется 'web')
.PHONY: shell
shell:
	$(DOCKER_COMPOSE) exec web /bin/bash

# Запуск миграций Django
.PHONY: migrate
migrate:
	$(DOCKER_COMPOSE) exec web python manage.py migrate

# Сбор статических файлов
.PHONY: collectstatic
collectstatic:
	$(DOCKER_COMPOSE) exec web python manage.py collectstatic --no-input

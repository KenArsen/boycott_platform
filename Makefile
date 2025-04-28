# Главный Makefile

# Включаем подфайлы для Nginx и Docker
include config/nginx/Makefile
include config/docker/Makefile

# Название проекта (используется только для вывода)
PROJECT_NAME = boycott_platform

.PHONY: help
help:
	@echo "Makefile для проекта: $(PROJECT_NAME)"
	@echo ""
	@echo "🛠️  Docker:"
	@echo "  make build               - Сборка Docker-образов"
	@echo "  make up                  - Запуск контейнеров в фоне"
	@echo "  make start               - Запуск контейнеров в обычном режиме (с логами)"
	@echo "  make stop                - Остановка контейнеров"
	@echo "  make down                - Остановка и удаление контейнеров"
	@echo "  make restart             - Перезапуск контейнеров"
	@echo "  make logs                - Просмотр логов контейнеров"
	@echo "  make clean               - Полная очистка: контейнеры, образы, тома"
	@echo "  make shell               - Доступ к bash в контейнере web"
	@echo ""
	@echo "🐍 Django:"
	@echo "  make migrate             - Выполнить миграции"
	@echo "  make create-superuser    - Создать суперпользователя"
	@echo "  make collectstatic       - Собрать статические файлы"
	@echo ""
	@echo "💾 Работа с данными (фикстуры):"
	@echo "  make dump APP=... FILE=... DIR=... - Экспортировать данные в JSON"
	@echo "  make load FILE=... DIR=...         - Импортировать данные из JSON"
	@echo ""
	@echo "🚀 Быстрая инициализация проекта:"
	@echo "  make init                - Билд, запуск, создание суперпользователя и загрузка данных"
	@echo ""
	@echo "🌐 Nginx:"
	@echo "  make deploy-nginx        - Задеплоить конфигурацию Nginx"
	@echo "  make remove-nginx        - Удалить конфигурацию Nginx"
	@echo "  make check-nginx-config  - Проверить синтаксис конфигурации"
	@echo "  make clear-logs          - Очистить логи Nginx"
	@echo ""
	@echo "🔧 Утилиты:"
	@echo "  make help                - Показать эту справку"



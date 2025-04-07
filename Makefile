# Главный Makefile

# Включаем подфайлы для Nginx и Docker
include config/nginx/Makefile
include config/docker/Makefile

# Команды для управления проектом

.PHONY: deploy remove check-config clear-logs

# Деплой конфигурации Nginx
deploy: deploy-nginx
	@echo "Nginx configuration deployed!"

# Удаление конфигурации Nginx
remove: remove-nginx
	@echo "Nginx configuration removed!"

# Проверка синтаксиса конфигурации Nginx
check-config: check-nginx-config
	@echo "Nginx configuration syntax checked!"

# Очистка логов Nginx
clear-logs: clear-logs
	@echo "Logs cleared!"

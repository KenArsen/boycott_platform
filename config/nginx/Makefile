# Пути к конфигурационным файлам Nginx
NGINX_CONF_FILE=config/nginx/boycott_platform.conf       # Локальный путь к файлу конфигурации Nginx проекта
NGINX_SITES_AVAILABLE=/etc/nginx/sites-available         # Стандартная папка для хранения доступных конфигураций
NGINX_SITES_ENABLED=/etc/nginx/sites-enabled             # Симлинки на активные конфигурации

# Деплой конфигурации Nginx:
# 1. Копирует конфиг в папку доступных сайтов
# 2. Создаёт симлинк в папке активных сайтов
# 3. Проверяет конфигурацию
# 4. Перезапускает Nginx
.PHONY: deploy-nginx
deploy-nginx:
	sudo cp $(NGINX_CONF_FILE) $(NGINX_SITES_AVAILABLE)/boycott_platform
	sudo ln -s $(NGINX_SITES_AVAILABLE)/boycott_platform $(NGINX_SITES_ENABLED)/boycott_platform
	sudo nginx -t
	sudo systemctl restart nginx

# Удаление конфигурации Nginx:
# 1. Удаляет симлинк из enabled
# 2. Удаляет сам файл из available
# 3. Перезапускает Nginx
.PHONY: remove-nginx
remove-nginx:
	sudo rm $(NGINX_SITES_ENABLED)/boycott_platform
	sudo rm $(NGINX_SITES_AVAILABLE)/boycott_platform
	sudo systemctl restart nginx

# Проверка корректности синтаксиса всех конфигурационных файлов Nginx
.PHONY: check-nginx-config
check-nginx-config:
	sudo nginx -t

# Очистка логов Nginx (access.log и error.log)
.PHONY: clear-logs
clear-logs:
	sudo rm -f /var/log/nginx/access.log /var/log/nginx/error.log

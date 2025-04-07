# config/nginx/Makefile

# Пути к конфигурационным файлам Nginx
NGINX_CONF_FILE=config/nginx/boycott_platform.conf
NGINX_SITES_AVAILABLE=/etc/nginx/sites-available
NGINX_SITES_ENABLED=/etc/nginx/sites-enabled

# Деплой конфигурации Nginx
.PHONY: deploy-nginx
deploy-nginx:
	sudo cp $(NGINX_CONF_FILE) $(NGINX_SITES_AVAILABLE)/boycott_platform
	sudo ln -s $(NGINX_SITES_AVAILABLE)/boycott_platform $(NGINX_SITES_ENABLED)/boycott_platform
	sudo nginx -t
	sudo systemctl restart nginx

# Удаление конфигурации Nginx
.PHONY: remove-nginx
remove-nginx:
	sudo rm $(NGINX_SITES_ENABLED)/boycott_platform
	sudo rm $(NGINX_SITES_AVAILABLE)/boycott_platform
	sudo systemctl restart nginx

# Проверка синтаксиса конфигурации Nginx
.PHONY: check-nginx-config
check-nginx-config:
	sudo nginx -t

# Очистка логов
.PHONY: clear-logs
clear-logs:
	sudo rm -f /var/log/nginx/access.log /var/log/nginx/error.log

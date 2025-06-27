#!/bin/bash

# Скрипт для настройки сервера
# Запускать с правами sudo

set -e

echo "Начинаем настройку сервера..."

# Обновление системы
echo "Обновление системы..."
apt update && apt upgrade -y

# Установка необходимых пакетов
echo "Установка пакетов..."
apt install -y python3 python3-pip python3-venv nginx postgresql postgresql-contrib redis-server git curl

# Настройка PostgreSQL
echo "Настройка PostgreSQL..."
sudo -u postgres psql -c "CREATE USER habit_user WITH PASSWORD 'habit_password';"
sudo -u postgres psql -c "CREATE DATABASE habit_tracker OWNER habit_user;"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE habit_tracker TO habit_user;"

# Настройка Redis
echo "Настройка Redis..."
systemctl enable redis-server
systemctl start redis-server

# Настройка файрвола
echo "Настройка файрвола..."
ufw allow ssh
ufw allow 'Nginx Full'
ufw --force enable

# Создание директории для приложения
echo "Создание директории приложения..."
mkdir -p /opt/habit-tracker
chown $SUDO_USER:$SUDO_USER /opt/habit-tracker

# Копирование файлов конфигурации
echo "Копирование конфигураций..."
cp habit-tracker.service /etc/systemd/system/
cp habit-tracker-nginx.conf /etc/nginx/sites-available/habit-tracker

# Настройка Nginx
echo "Настройка Nginx..."
ln -sf /etc/nginx/sites-available/habit-tracker /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default
nginx -t
systemctl restart nginx

# Настройка systemd сервисов
echo "Настройка systemd сервисов..."
systemctl daemon-reload
systemctl enable habit-tracker

echo "Настройка сервера завершена!"
echo "Теперь выполните следующие шаги:"
echo "1. Клонируйте репозиторий в /opt/habit-tracker"
echo "2. Создайте виртуальное окружение"
echo "3. Установите зависимости"
echo "4. Настройте .env файл"
echo "5. Примените миграции"
echo "6. Запустите сервисы" 
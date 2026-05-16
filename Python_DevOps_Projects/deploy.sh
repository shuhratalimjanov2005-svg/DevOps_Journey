#!/bin/bash

# 🔥 УМНАЯ ПРОВЕРКА: Если команды docker-compose нет, скрипт САМ её установит!
if ! command -v docker-compose &> /dev/null
then
    echo "⚠️ Старый docker-compose не найден! Исправляем..."
    sudo curl -L "https://github.com/docker/compose/releases/download/v2.24.5/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
    echo "✅ docker-compose успешно установлен в систему!"
fi

echo " Запуск сборки Docker Compose..."
docker-compose down
docker-compose up -d --build

echo " Всё готово! Контейнеры подняты в фоне в твоей виртуалке!"
